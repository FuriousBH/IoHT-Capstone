#Original concept code from: https://github.com/nidhog/dreamcatcher/blob/master/application.py

# Python application to host flask app on local host and use OAuth2 to retrieve user data from
# Oura API.
import os
import csv
import json
import requests
import sys
import boto3
from flask import Flask, session, redirect, request, url_for
from requests_oauthlib import OAuth2Session
import pandas as pd
from dotenv import load_dotenv
from waitress import serve

#load tokens from env
load_dotenv()

application = Flask(__name__)

#assigning URLs to variables and getting tokens from env
OURA_CLIENT_ID     = os.getenv('OURA_CLIENT_ID')
OURA_CLIENT_SECRET = os.getenv('OURA_CLIENT_SECRET')
OURA_AUTH_URL = 'https://cloud.ouraring.com/oauth/authorize'
OURA_TOKEN_URL = 'https://api.ouraring.com/oauth/token'


#Login to the Oura cloud.
#This will redirect to the login page of the OAuth provider
@application.route('/login')
def oura_login():
    
    oura_session = OAuth2Session(OURA_CLIENT_ID)

    # URL for Oura's authorization page for specific client
    authorization_url, state = oura_session.authorization_url(OURA_AUTH_URL)

    session['oauth_state'] = state

    return redirect(authorization_url)

#This is where the Oura API redirects to after authorization
@application.route('/callback')
def callback():
#Callback page Get the acces_token from response url from Oura. 
    
    oura_session = OAuth2Session(OURA_CLIENT_ID, state=session['oauth_state'])
    session['oauth'] = oura_session.fetch_token(
                        OURA_TOKEN_URL,
                        client_secret=OURA_CLIENT_SECRET,
                        authorization_response=request.url)
    return redirect(url_for('.heartrate'))
                            #.sleep

#This is where the webapp makes the API request for data
@application.route('/heartrate')
def heartrate():
    #get heartrate data from the Oura api
    oauth_token = session['oauth']['access_token']

    url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
    params={ 
        'start_datetime': '2022-03-21T00:00:00-08:00', 
        'end_datetime': '2022-03-23T00:00:00-08:00' 
    }
    headers = { 
        'Authorization': 'Bearer ' + oauth_token, 
    }
    response = requests.request('GET', url, headers=headers, params=params) 
    print (response.text)
    
    #convert response to text to json
    rawData = response.text
    json_data = json.loads(rawData)

    #write response json to result.json file
    with open('result.json', 'w') as file:
        json.dump(json_data, file, indent =4)

    #TEMPORARILY DISABLED, trying to combine code into as few files as possible
    #adds person ID to dictionaries
    exec(open("jsonAddKeyValuePair.py").read())

    #converts json file into csv file
    exec(open("jsonToCSV.py").read())

    #uploads oura csv to dynamo db
    exec(open("csvToDynamoDB.py").read())

    return "<h1>The birds work for the bourgeoisie</h1>"


#home page
@application.route('/')
def home():
    return "<h1>Welcome to your Oura application</h1>"

if __name__ == "__main__":

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    application.secret_key = os.urandom(24)
    #old flask code
    #application.run(debug=False, host='127.0.0.1', port=8080)
    serve(application, host='0.0.0.0', port=80)
                                        #port=8080 for testing