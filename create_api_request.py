"""create a simple api request out of inline user input"""

import argparse
import subprocess
import json
import configparser

config = configparser.ConfigParser()
config.read("static_files/config.ini")
viessmann_access_token = config["viessmann"]["viessmann_access_token"]


parser = argparse.ArgumentParser(
    description="create a simple api request out of inline user input coming after 'https://api.viessmann.com/iot/v1/equipment/installations'"
)

parser.add_argument("statement", type=str)

args = parser.parse_args()
statement = str(args.statement)


def process_api_request(statement, print_statement=False):
    prefix = "curl -X GET https://api.viessmann.com"
    suffix = ' -H "Authorization: Bearer ' + viessmann_access_token + '"'
    terminal_statement = prefix + statement + suffix

    if print_statement:
        print(terminal_statement)

    output = subprocess.check_output(terminal_statement, shell=True)
    output_json = json.loads(output)
    return output_json


output_json = process_api_request(statement, print_statement=True)
print(json.dumps(output_json, indent=4))
