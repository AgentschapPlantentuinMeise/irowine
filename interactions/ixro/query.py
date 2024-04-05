import os
import time
from urllib.request import urlretrieve
import requests

query_original = '''
{{
  "sendNotification": true,
  "notificationAddresses": [
    "{email}"
  ],
  "format": "SQL_TSV_ZIP",
  "sql": "SELECT \
    PRINTF('%04d-%02d', \\"year\\", \\"month\\") AS yearMonth,\
    GBIF_EEARGCode(\
      1000,\
      decimalLatitude,\
      decimalLongitude,\
      COALESCE(coordinateUncertaintyInMeters, 1000)\
      ) AS eeaCellCode,\
    familyKey,\
    family,\
    speciesKey,\
    species,\
    datasetKey,\
    COALESCE(sex, 'NOT_SUPPLIED') AS sex,\
    COALESCE(occurrence.lifestage.concept, 'NOT_SUPPLIED') AS lifestage, \
    COUNT(*) AS occurrences\
  FROM\
    occurrence\
  WHERE\
    countryCode = '{countryCode}'\
    AND occurrenceStatus = 'PRESENT'\
    AND \\"year\\" >= 2000\
    AND hasCoordinate = TRUE\
    AND speciesKey IN ({speciesKeyList})\
    AND NOT ARRAY_CONTAINS(issue, 'ZERO_COORDINATE')\
    AND NOT ARRAY_CONTAINS(issue, 'COORDINATE_OUT_OF_RANGE')\
    AND NOT ARRAY_CONTAINS(issue, 'COORDINATE_INVALID')\
    AND NOT ARRAY_CONTAINS(issue, 'COUNTRY_COORDINATE_MISMATCH')\
    AND \\"month\\" IS NOT NULL\
  GROUP BY\
    yearMonth,\
    datasetKey,\
    eeaCellCode,\
    familyKey,\
    family,\
    speciesKey,\
    species,\
    sex,\
    lifestage\
  ORDER BY\
    yearMonth DESC,\
    eeaCellCode ASC,\
    speciesKey ASC;\
    "
}}
'''

query_template = '''
{{
  "sendNotification": true,
  "notificationAddresses": [
    "{email}"
  ],
  "format": "SQL_TSV_ZIP",
  "sql": "SELECT \
    datasetKey,\
    GBIF_EEARGCode(\
      1000,\
      decimalLatitude,\
      decimalLongitude,\
      COALESCE(coordinateUncertaintyInMeters, 1000)\
      ) AS eeaCellCode,\
    speciesKey,\
    species,\
    COUNT(*) AS occurrences\
  FROM\
    occurrence\
  WHERE\
    countryCode = '{countryCode}'\
    AND occurrenceStatus = 'PRESENT'\
    AND hasCoordinate = TRUE\
    AND speciesKey IN ('{speciesKeyList}')\
  GROUP BY\
    datasetKey,\
    eeaCellCode,\
    speciesKey,\
    species,\
    "
}}
'''

query_dict = {
  "sendNotification": False,
  "notificationAddresses": [ 
  ],
  "format": "SQL_TSV_ZIP", 
  "sql": "SELECT PRINTF('%04d-%02d', \"year\", \"month\") AS yearMonthdatasetKey, speciesKey, GBIF_EEARGCode(1000,decimalLatitude,decimalLongitude,COALESCE(coordinateUncertaintyInMeters, 1000) AS eeaCellCode,COUNT(*) FROM occurrence WHERE countryCode = 'BE' AND speciesKey IN (2578415,3204123,2049512,8107588,5372392) GROUP BY datasetKey, speciesKey" 
}

def cube_query(email, country, speciesKeyList, query_template=query_original):
    query = query_template(
        email=email, countryCode=country,
        speciesKeyList=','.join(speciesKeyList)
    )
    #with open('query.json','wt') as qf:
    #    qf.write(query)
    headers = {
        'Content-type': 'application/json',
        #'Accept': 'text/plain'
    }
    r_valid = requests.post(
        'https://api.gbif.org/v1/occurrence/download/request/validate',
        data=query, headers=headers
    )
    if r_valid.status_code > 201:
        raise Exception(r_valid.status_code)
    r_cube = requests.post(
        'https://api.gbif.org/v1/occurrence/download/request',
        data=query, headers=headers,
        auth = (
            os.environ.get('GBIF_USER'),
            os.environ.get('GBIF_PWD')
        )
    )
    if r_cube.status_code > 201:
        raise Exception(r_cube.status_code)
    return r_cube.text # cube job id

def download_cube(cube_job_id, prefix):
    while (r:=json.loads(requests.get(
        f"https://api.gbif.org/v1/occurrence/download/{cube_job_id}"
    ).text))['status'] == 'RUNNING':
        time.sleep(60)
    if r['status'] != 'SUCCEEDED':
        raise Exception(r['status'])
    urlretrieve(
        r['downloadLink'],
        prefix+r['downloadLink'][r['downloadLink'].rindex('/')+1:]
    )

#curl --include --header "Content-Type: application/json" --data @query.json https://api.gbif.org/v1/occurrence/download/request/validate

#curl --include --user 'maxime_ryckewaert':'password' --header "Content-Type: application/json" --data @query.json https://api.gbif.org/v1/occurrence/download/request
