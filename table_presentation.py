'''
    ** Coding challenge **
    Requirement:
        - Get a list of Adobe public repo on github
        - Print then into table format in the command line
        - Table should be sorted by most recently updated
        - Include any field in the table format
    Date: 08/04/2021
'''
import os
import sys
import json
import requests
import pandas as pd
from argparse import ArgumentParser


options = None


def parse_options(args):
    ''' Function to provide consolidated option list '''
    usage = "usage: %prog [options] args"
    parser = ArgumentParser(description='Show records in table format')

    parser.add_argument("-ep", "--endpoint",
                        action="store", dest="endpoint",
                        type=str,
                        help="Provide publich end point")

    args = globals()["options"] = parser.parse_args(args)

    return args


def getRecordsInTabularForm():
    '''
        Get repos in sorted order by last updated in tabular form
        Return: dataframe
    '''
    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    # Do the HTTP request
    response = requests.get(options.endpoint, headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:',
              response.headers, 'Error Response:', response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = json.dumps(response.json())
    df = pd.DataFrame.from_dict(json.loads(data))
    return df


''' Main function starts here '''


def main():
    parse_options(sys.argv[1:])
    # Setting default endpoint
    if not options.endpoint:
        options.endpoint = 'https://api.github.com/orgs/adobe/repos'
    df = getRecordsInTabularForm()
    print('')
    print(f"Records listed as per updated date, records shape: {df.shape}")

    print(df.sort_values(by=['updated_at'], ascending=False)[
          ["updated_at", "stargazers_count"]])


if __name__ == '__main__':
    main()
