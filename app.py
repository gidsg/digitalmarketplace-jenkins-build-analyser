import ast
import requests
from dotenv import load_dotenv
import os
load_dotenv()

r = requests.get("https://ci.marketplace.team/job/release-admin-frontend/api/python?tree=allBuilds["
                 "number,id,timestamp,result,duration]",
                 auth=(os.getenv('JENKINS_USERNAME'),
                       os.getenv('JENKINS_API_TOKEN')))
builds = ast.literal_eval(r.text)
successful_builds = list(filter(lambda b: b['result'] == 'SUCCESS', builds['allBuilds']))
print(successful_builds)


