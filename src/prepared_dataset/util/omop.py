import requests
import time
import config

verify = False

if config.FHIR_PREPROC_PW is not None:
    auth = (config.FHIR_PREPROC_USER, config.FHIR_PREPROC_PW)
else:
    auth = None

def get_omop_data(patient_ids, omop_config):
    feature_set = []

    r = requests.post(config.FHIR_URL + '/crawler', json={"patient": patient_ids, "feature_set": omop_config['feature_set']}, verify=verify, auth=auth)
    crawler_info = r.json()

    json_url = crawler_info["csv_url"].replace("csv", "json")


    json_url = config.FHIR_URL + "/aggregation/" + crawler_info["crawler_id"] + "?output_type=json&aggregation_type=latest"
    r = requests.get(json_url, verify=verify, auth=auth)

    while r.status_code == 404:
        print(json_url)
        print("got statuscode 404")
        r = requests.get(json_url, verify=verify, auth=auth)
        time.sleep(1)
        

    omop_data = r.json()


    ret = {}

    for pid in patient_ids:
        for o in omop_data:
            if o["patient_id"] == pid:
                ret[pid] = o
                break

    return ret
