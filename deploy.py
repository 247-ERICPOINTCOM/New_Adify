
'''
For more information on the endpoints check:
https://help.pythonanywhere.com/pages/API#consoles

Used to run the deployment script from the a local environment

''' 

import json
import requests
import environ
import os
from pathlib import Path

# Get the environment values
env_file = os.path.join(Path(__file__).resolve().parent,".env")
env = environ.Env()
env.read_env(env_file)

username = env('PYTHONANYWHERE_USER')
token = env('PYTHONANYWHERE_API_KEY')
host = env('PYTHONANYWHERE_HOST')
domain_name = env('PYTHONANYWHERE_DOMAIN')


# Check for the active console instances
response = requests.get(
    f'https://{host}/api/v0/user/{username}/consoles/',
    headers={'Authorization': 'Token {token}'.format(token=token)}
)

if response.status_code != 200:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

response_json = json.loads(response.content.decode('UTF-8'))
consoles_active = len(response_json)

print(f"There are currently have {consoles_active} console(s) active.\n")
if consoles_active > 0:
    for num,console in enumerate(response_json):
        print(f"({num}) ID:{console['id']}\tname:{console['name']}")
else:
    print("Please turn on a console on pythonanywhere")
    exit()



# Pick a console to run the deployment script
try:
    while True:
        console_num = int(input("\nWhich console would you like to use? (num): "))
        if (console_num > consoles_active) or (console_num < 0):
            print("please give a valid index for the console")
        else:
            id=response_json[console_num]['id']
            break
except:
    print("\n Error in input")
    exit()


# Pick a console to run the deployment script
print(f"Attempting app deployment using {response_json[console_num]['name']}...")

data = {
        "input":"cd ~/adify && git pull \n"
}
response = requests.post(
        f'https://{host}/api/v0/user/{username}/consoles/{id}/send_input/',
        headers={'Authorization': 'Token {token}'.format(token=token)} ,
        data=data
        )

if response.status_code != 200:
    print("Failed to send input. Status code:", response.status_code)

print("Input sent successfully.\n")

# TODO: Will the git pull finish before we get to this point for the webapp reload? 

# print("Reloading the webapp remotely...")
#
# response = requests.post(
#         f'https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/',
#         headers={'Authorization': 'Token {token}'.format(token=token)} ,
#         )
#
# if response.status_code != 200:
#     print("Failed to send input. Status code:", response.status_code)
#
# print("Reload sent successfully.")
# print("Please allow a few seconds for server to reflect changes...")
