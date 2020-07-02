import ast
import requests
from dotenv import load_dotenv
import os
import csv
import datetime
import statistics

load_dotenv()
pipelines = ['release-admin-frontend',
             'release-antivirus-api',
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


filename = 'output.csv'
all_successful_builds = list()

with open(filename, 'w') as csv_file:
    fieldnames = ['pipeline', 'run_id', 'timestamp (UNIX)', 'duration (milliseconds)']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for pipeline in pipelines:
        r = requests.get(f"https://ci.marketplace.team/job/{pipeline}/api/python?tree=allBuilds["
                         "id,timestamp,result,duration]",
                         auth=(os.getenv('JENKINS_USERNAME'),
                               os.getenv('JENKINS_API_TOKEN')))
        builds = ast.literal_eval(r.text)
        successful_builds = list(filter(lambda b: b['result'] == 'SUCCESS', builds['allBuilds']))
        print(successful_builds)
        all_successful_builds.extend(successful_builds)
        for sb in successful_builds:
            writer.writerow({'pipeline': pipeline,
                             'run_id': sb['id'],
                             'timestamp (UNIX)': sb['timestamp'],
                             'duration (milliseconds)': sb['duration']
                             })

print(f"Results written to: {os.getcwd()}/{filename}")
print("Total successful builds: " + str(len(all_successful_builds)))
duration_list = list(map(lambda x: x['duration'], all_successful_builds))
print("Average total runtime: " + time_formatter(statistics.mean(duration_list)))
print("Mean total runtime: " + time_formatter(statistics.median_low(duration_list)))
