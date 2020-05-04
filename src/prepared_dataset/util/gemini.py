import requests
import time
import config

COLUMN_NAME_SEPARATOR = "#"

if config.GEMINI_PW is not None:
    auth = (config.GEMINI_USER, config.GEMINI_PW )
else:
    auth = None


gemini_base = config.GEMINI_URL
verify = False


def get_gemini_data(patient_ids, gemini_config):

    gemini_dbs = get_all_gemini_dbs()


    if gemini_config['sql_mode'] == True:
        return get_gemini_data_from_sql(patient_ids,gemini_config, get_relevant_patient_dbs(patient_ids, gemini_dbs))

    else:
        key_names = ["chrom", "start", "end", "alt"]
        column_list = list(set(gemini_config["variants"]["columns"]).union(set(key_names)))
        columns = ", ".join(column_list)
        where_parts = []
        for k in gemini_config["variants"]["keys"]:
            where_parts.append(
                """
                    (chrom = '{}' AND start = '{}' AND end = '{}' AND alt = '{}')
                """.format(k["chrom"], k["start"], k["end"], k["alt"])
            )
        where = " or ".join(where_parts)

        query = """
        select {}
        from variants
        where {}
        limit -1
        """.format(columns, where)

       

        if gemini_config["database"]["merged"]:
            return get_merged_db_variants_data(patient_ids, get_merged_db(gemini_dbs, gemini_config["database"].get("name")), query, gemini_config["variants"]["keys"], key_names, gemini_config["variants"]["columns"])
        else:
            return get_single_patient_dbs_variants_data(patient_ids, get_relevant_patient_dbs(patient_ids, gemini_dbs), query, gemini_config["variants"]["keys"], key_names, gemini_config["variants"]["columns"])


def get_gemini_data_from_sql(patient_ids, gemini_config, dbs):

    ret = {}
    query = gemini_config['sql']
    column_selectors = gemini_config['columns']
    row_selectors = gemini_config['rows']

    for pid in patient_ids:
        gemini_data = []
        if pid in dbs:
            gemini_data = query_gemini_data(dbs[pid], query)

        tmp = combine_pat_id_with_gemini_data(pid, gemini_data, row_selectors, column_selectors)
        ret[pid] = tmp

    return ret


def combine_pat_id_with_gemini_data(pid, gemini_data, row_selectors, column_selectors):

    tmp = {"patient_id": pid, "entries": []}

    for row in gemini_data:

        column_name = ""
        
        for column_selector in column_selectors:
            column_name = column_name + COLUMN_NAME_SEPARATOR + row[column_selector]

        for row_selector in row_selectors:
            tmp['entries'].append({column_name: row[row_selector]})

        return tmp



def get_all_gemini_dbs():

    r = requests.get(gemini_base + "/dbs", verify=verify, auth=auth)
    return r.json()


def get_merged_db(dbs, db_name):
    print(db_name, flush=True)
    for db in dbs:
        print(db, flush=True)
        if db.endswith("_merged"):
            if db_name is None:
                return db
            elif db_name == db:
                return db
    raise Exception(f"no merged gemini db for for name parameter {db_name} found")


def get_relevant_patient_dbs(patient_ids, dbs):
    ret = {}
    for db in dbs:
        if db.endswith("_merged"):
            continue
        if db in patient_ids:
            ret[db] = db
            continue

        if "_pid_" in db:
            if db.find("_pid_") != db.rfind("_pid_"):
                continue

            db_split = db.split("_pid_")
            if int(db_split[1]) in patient_ids:
                ret[int(db_split[1])] = db
    
    return ret


def get_single_patient_dbs_variants_data(patient_ids, dbs, query, keys, key_names, column_names):
    ret = {}

    for pid in patient_ids:
        gemini_data = []
        if pid in dbs:
            gemini_data = query_gemini_data(dbs[pid], query)

        tmp = combine_patient_id_with_gemini_data(pid, keys, key_names, gemini_data, column_names)
        ret[pid] = tmp

    return ret


def get_merged_db_variants_data(patient_ids, db, query, keys, key_names, column_names):
    ret = {}

    samples_query = """
    select name
    from samples
    order by sample_id asc
    limit -1
    """

    samples_data = query_gemini_data(db, samples_query)
    sample_position_patient_id = {}
    cnt = 0
    for sd in samples_data:
        pid = int(sd["name"].split("_pid_")[1])
        sample_position_patient_id[cnt] = pid
        cnt += 1

    gemini_data = query_gemini_data(db, query)
    for pid in patient_ids:
        tmp = combine_patient_id_with_gemini_data(pid, keys, key_names, gemini_data, column_names, merged_db=True, sample_position_patient_id=sample_position_patient_id)
        ret[pid] = tmp

    return ret


def query_gemini_data(db, query):

    r = requests.post(gemini_base + "/query", json={"db_name": db, "query": query}, verify=verify, auth=auth)

    if r.status_code == 400:
        print("database with id corrupt: " + db)
        return []

    return r.json()["data"]


def combine_patient_id_with_gemini_data(pid, keys, key_names, gemini_data, column_names, merged_db=False, sample_position_patient_id={}):
    tmp = {"patient_id": pid, "entries": []}
    for k in keys:
        key_values = []
        for kn in key_names:
            key_values.append(k[kn])
        prefix = COLUMN_NAME_SEPARATOR.join(key_values)
        match = False
        for d in gemini_data:
            if not (k["chrom"] == d["chrom"] and k["start"] == d["start"] and k["end"] == d["end"]):
                continue
            match = True
            for cn in column_names:
                insert_value = None
                if merged_db and cn.startswith("gt"):
                    data_split = d[cn].split(",")
                    i = 0
                    for ds in data_split:
                        if i in sample_position_patient_id and sample_position_patient_id[i] == pid:
                            insert_value = ds
                            break
                        i += 1
                else:
                    insert_value = d[cn]
                tmp["entries"].append({prefix + COLUMN_NAME_SEPARATOR + cn: insert_value})
        if not match:
            for cn in column_names:
                tmp["entries"].append({prefix + COLUMN_NAME_SEPARATOR + cn: None})
    return tmp
