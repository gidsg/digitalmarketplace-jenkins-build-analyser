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


def time_formatter(milliseconds):
    td = datetime.timedelta(milliseconds=milliseconds)
    seconds = td.total_seconds()
    hours = seconds // 3600
    return f"{hours} hours"


with open('output.csv', 'w') as csv_file:
    all_successful_builds = list()
    row_count = 0
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
        print(successful_builds)
        all_successful_builds.extend(successful_builds)
        for sb in successful_builds:
            writer.writerow({'pipeline': pipeline, 'run_id': sb['id'], 'duration': sb['duration']})

    print("Total successful builds: " + str(len(all_successful_builds)))
    average_duration = sum(list(map(lambda x: x['duration'], all_successful_builds))) / len(all_successful_builds)
    print("Average total runtime: " + str(time_formatter(average_duration)))
