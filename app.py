import ast
import requests
from dotenv import load_dotenv
import os
import csv
import datetime

load_dotenv()
pipelines = ['release-antivirus-api',
             'release-admin-frontend',
             'release-api',
             'release-brief-responses-frontend',
             'release-briefs-frontend',
             'release-buyer-frontend',
             'release-router',
             'release-search-api',
             'release-supplier-frontend',
             'release-user-frontend',
             ]


def milliseconds_to_hours(milliseconds):
    td = datetime.timedelta(milliseconds=milliseconds)
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60


with open('output.csv', 'w') as csv_file:
    fieldnames = ['pipeline', 'run_id', 'duration']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for pipeline in pipelines:
        r = requests.get(f"https://ci.marketplace.team/job/{pipeline}/api/python?tree=allBuilds["
                         "number,id,timestamp,result,duration]",
                         auth=(os.getenv('JENKINS_USERNAME'),
                               os.getenv('JENKINS_API_TOKEN')))
        builds = ast.literal_eval(r.text)
        successful_builds = list(filter(lambda b: b['result'] == 'SUCCESS', builds['allBuilds']))
        for sb in successful_builds:
            writer.writerow({'pipeline': pipeline, 'run_id': sb['id'], 'duration': sb['duration']})
            print(successful_builds)
