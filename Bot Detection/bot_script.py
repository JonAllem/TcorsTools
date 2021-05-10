# Bot detection using the botometer API.
import pandas as pd
import numpy as np
import tqdm as tqdm
import botometer
import pickle
import os

# Start and end index of the users list.
start = 0
end = 214514

print("Starting at: " + str(start))
print("Ending at: " + str(end))
print("Total: " + str(end - start))

# Input is the csv file containing just the user-ids of Twitter Users.
unique_users = pd.read_csv(r"D:\users\users.csv")
unique_users = unique_users['0']

# Add your RapidAPI credentials and Twitter API credentials below.
rapidapi_key = "RAPIDAPI_KEY"
twitter_app_auth = {
    'consumer_key': 'CONSUMER_KEY',
    'consumer_secret': 'CONSUMER_SECRET'
  }
api_url = 'https://botometer-pro.p.mashape.com'
bom = botometer.Botometer(botometer_api_url=api_url,wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

account_scores = {}
count = 0
oldFile = ''
for screenname, result in  tqdm.tqdm(bom.check_accounts_in(unique_users[start:end])):
    if 'error' in result:
        account_scores[screenname] = None
    else:
        account_scores[screenname] = result
    count+=1
    # Output is stored in temp files in case the program is stopped midway
    if count % 1000 == 0:
        with open('temp_account_scores_' + str(start) + '_' + str(start + count) + '.pickle', 'wb') as file:
            pickle.dump(account_scores, file)
        if oldFile != '':
            os.remove(oldFile)
        oldFile = 'temp_account_scores_' + str(start) + '_' + str(start + count) + '.pickle'

# Store final output in pickle files.
with open('account_scores_' + str(start) + '_' + str(end) + '.pickle', 'wb') as file:
    pickle.dump(account_scores, file)
if oldFile != '':
    os.remove(oldFile)