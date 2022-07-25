import requests
import json
import os
 
# Authenticate yourself with the token.
# Remember to follow your organization's security standards when handling the token.   
auth_token = os.getenv('VH_API_TOKEN')
headers = {'authorization': 'token %s' % auth_token}
project_id = '01822558-83c3-f0ed-ee27-1e68c5a7d0aa'
step_name = 'train-model'
 
# Fetch all new changes from the repository
# https://app.valohai.com/api/docs/#projects-fetch
# This will fetch changes from all the branches that you've defined on the Project->Settings->Repository tab
fetchResponse = requests.post(('https://app.valohai.com/api/v0/projects/{0}/fetch/').format(project_id), data={'id': project_id}, headers=headers)
fetchResponse.raise_for_status()
 
# Define the payload for a new execution
# https://app.valohai.com/api/docs/#executions-create
#
# GitHub Actions creates an environment variable on the Docker container
# Called GITHUB_SHA that stores the identifier of the commit that was created
new_exec_payload = {
   "project": project_id,
   "commit": os.getenv('GITHUB_SHA'),
   "step": step_name
}
 
# Send a POST request to create a new execution
createExecutionResponse = requests.post('https://app.valohai.com/api/v0/executions/', json=new_exec_payload, headers=headers)
createExecutionResponse.raise_for_status()
 
# Print the response you've received back
print('# API Response:\n')
print(json.dumps(createExecutionResponse.json(), indent=4))
