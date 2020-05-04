from util import gemini, omop
import io
import csv
from flask import send_file
import tempfile

def get_omop_gemini_combined(format, patient_ids, omop_config, gemini_config):
    ret = []

    omop_data = omop.get_omop_data(patient_ids, omop_config)
    gemini_data = gemini.get_gemini_data(patient_ids, gemini_config)

    for pid in patient_ids:
        tmp = {"patient_id": pid}
        tmp["fhir"] = omop_data.get(pid)
        tmp["gemini"] = gemini_data.get(pid)
        ret.append(tmp)

    if format == "json":
        return ret

    omop_col_names = extract_column_names_fhir(omop_data)
    gemini_col_names = extract_column_names(gemini_data)
    csv_file = create_csv(omop_col_names, gemini_col_names, ret)

    return send_file(csv_file.name, mimetype='text/comma-separated-values', as_attachment=True)

def create_csv(omop_col_names, gemini_col_names, ret_data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["patient_id"] + omop_col_names + gemini_col_names)
    for d in ret_data:
        to_write = [d["patient_id"]]
        if d["fhir"]:
            for column_name in omop_col_names:
                inserted = False
                for e in d["fhir"]["entries"]:
                    for key, value in e.items():
                        if key == column_name:
                            to_write.append(value)
                            inserted = True
                if not inserted:
                    to_write.append(None)
        else:
            for column_name in omop_col_names:
                    to_write.append(None)
        if d["gemini"]:
            for column_name in gemini_col_names:
                inserted = False
                for e in d["gemini"]["entries"]:
                    for key, value in e.items():
                        if key == column_name:
                            to_write.append(value)
                            inserted = True
                if not inserted:
                    to_write.append(None)
            
        writer.writerow(to_write)
    tmp_csv = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    with open(tmp_csv.name, 'w') as f:
        f.write(output.getvalue())
    return tmp_csv

def extract_column_names(data):

    col_names = {}

    for value in data.items():
        
        if value[1] is None:
            continue

        for entry in value[1]['entries']:
            for key in entry.keys():
                col_names[key] = 1

    return list(col_names.keys())

def extract_column_names_fhir(data):

    col_names = {}

    for value in data.items():

        if value is None:
            continue

        for entry in value[1]['entries']:
            for key in entry.keys():
                col_names[key] = 1

    return list(col_names.keys())

