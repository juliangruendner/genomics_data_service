import subprocess
import yaml
import os
import flask
import re


config = yaml.load(open('config.yml'))


def _execute_gemini_command(cmd):
    cmd = ["gemini"] + cmd
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8").rstrip()
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.output, flush=True)
        raise exc


def query_cli(db_path, query, skip, limit, jsonify=True):
    if skip is None:
        skip = 0
    if limit is None:
        limit = -1

    cmd = ["query"]
    if "--header" not in query:
        cmd.append("--header")
    cmd.append("-q")
    query = query.replace('query -q', '')
    query = query.rstrip()

    match = re.search('"(.+?)"', query)
    select_statement = None
    if match:
        select_statement = match.group(1)
    if select_statement is not None:
        query = query.replace('"' + select_statement + '"', '')
        if "limit" not in select_statement and "--gt" not in query:
            select_statement += " limit " + str(limit)
        if "offset" not in select_statement and "--gt" not in query:
            select_statement += " offset " + str(skip)
        cmd.append(select_statement)
    query = query.replace('"', ' ')
    cmd = cmd + query.split()
    cmd.append(db_path)
    output = _execute_gemini_command(cmd)
    if not jsonify:
        return output.splitlines()
    return _jsonify_query_output(output)


def _jsonify_query_output(output):
    # build JSON myself to maintain correct order
    # json_dumps with dicts would screw up the order
    output = output.splitlines()
    ret = "["
    headers = output[0].split("\t")
    for i in range(1, len(output)):
        ret += "{"
        tmp = output[i].split("\t")
        for idx, val in enumerate(tmp):
            ret += '"' + headers[idx] + '":"' + val.replace('\\', '\\\\') + '"'
            if idx < len(tmp)-1:
                ret += ','
        ret += "}"
        if i < len(output)-1:
            ret += ','
    ret += "]"
    return ret


def query(db_name, query, skip, limit):
    query = query.replace('\r\n', ' ')
    query = query.replace('\n', ' ')
    if '"' not in query:
        query = '"' + query + '"'
    db_path = os.path.join(config["DBS_PATH"], db_name)
    ret_query = query_cli(db_path, query, skip, limit)
    count = 1
    if "--gt" not in query:
        match = re.search('select(.+?)from', query, re.IGNORECASE)
        select_clause = None
        if match:
            select_clause = match.group(1)
        query_count = None
        if select_clause is not None:
            query_count = query.replace(select_clause, " count(*) ")
        ret_count = query_cli(db_path, query_count, None, None, False)
        count = ret_count[1]
    ret = '{"count":' + str(count) + ', "data":' + ret_query + '}'
    return ret


def query_variants(db_name, skip, limit):
    select_statement = """
    "select *, (gts).(*), (gt_types).(*), (gt_phases).(*), (gt_depths).(*), (gt_ref_depths).(*), (gt_alt_depths).(*), (gt_alt_freqs).(*), (gt_quals).(*) from variants"
    """
    return query(db_name, select_statement, skip, limit)


def get_gemini_dbs():
    dbs = [f for f in os.listdir(config["DBS_PATH"]) if os.path.isfile(os.path.join(config["DBS_PATH"], f))]
    return dbs


def get_vcf_files():
    vcf_files = [
        f for f in os.listdir(config["VCFS_PATH"]) if
        os.path.isfile(os.path.join(config["VCFS_PATH"], f)) and
        os.path.join(config["VCFS_PATH"], f).endswith(".vcf")
    ]
    return vcf_files


def send_gemini_db(db_name):
    response = flask.send_from_directory(config["DBS_PATH"], db_name, as_attachment=True)
    response.headers['content-type'] = 'application/octet-stream'
    response.status_code = 200
    return response


def send_vcf(vcf_name):
    response = flask.send_from_directory(config["VCFS_PATH"], vcf_name, as_attachment=True)
    response.status_code = 200
    return response


def make_directories():
    if not os.path.exists(config["VCFS_PATH"]):
        os.makedirs(config["VCFS_PATH"])
    if not os.path.exists(config["DBS_PATH"]):
        os.makedirs(config["DBS_PATH"])


def execute_pipeline(vcf_file, db_name):
    db_name = db_name.replace(' ', '')
    vcf_file = os.path.join(config["VCFS_PATH"], vcf_file)
    vcf_ann_file = os.path.join(vcf_file.replace(".vcf", ".ann.vcf.gz"))
    db_file = os.path.join(config["DBS_PATH"], db_name)
    subprocess.call(["./util/pipeline.sh", vcf_file, config["HG19_REF_FILE"], config["SNPEFFJAR"], vcf_ann_file, db_file])
    return db_file


def load_vcf_files(files):
    for f in files:
        vcf_file = os.path.join(config["VCFS_PATH"], f.filename)
        f.save(vcf_file)


def bgzip_tabix_vcf_file(vcf_file):
    subprocess.call(["./util/bgzip_and_tabix.sh", vcf_file])
    return vcf_file + ".gz"


def bcf_tools_merge(vcf_files, out_file, filter_option):
    if filter_option is None or filter_option != "x":
        filter_option = "+"
    else:
        filter_option = "x"
    subprocess.call(["./util/bcf_merge.sh", out_file, filter_option] + [str(f) for f in vcf_files])


def vcf_merge(vcf_files, out_file):
    subprocess.call(["./util/vcf_merge.sh", out_file] + [str(f) for f in vcf_files])


def merge(tool, filter_option, vcf_files, out_file):
    out_file = out_file.replace(' ', '')
    out_file = os.path.join(config["VCFS_PATH"], out_file)
    if not out_file.endswith(".vcf"):
        out_file += ".vcf"
    vcf_files_tmp = []
    for fn in vcf_files:
        vcf_files_tmp.append(os.path.join(config["VCFS_PATH"], fn))
    vcf_files = vcf_files_tmp
    vcf_files_gz = []
    for fn in vcf_files:
        vcf_files_gz.append(bgzip_tabix_vcf_file(fn))
    if tool == "bcf":
        return bcf_tools_merge(vcf_files_gz, out_file, filter_option)
    elif tool == "vcf":
        return vcf_merge(vcf_files_gz, out_file)
    else:
        raise Exception("unknown tool string")
