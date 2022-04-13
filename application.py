#Original concept code from: https://github.com/nidhog/dreamcatcher/blob/master/application.py

# Python application to host flask app on local host and use OAuth2 to retrieve user data from
# Oura API.
import os
import csv
import json
import requests
from flask import Flask, session, redirect, request, url_for
from requests_oauthlib import OAuth2Session
import pandas as pd
from dotenv import load_dotenv
from waitress import serve

load_dotenv()

application = Flask(__name__)


OURA_CLIENT_ID     = os.getenv('OURA_CLIENT_ID')
OURA_CLIENT_SECRET = os.getenv('OURA_CLIENT_SECRET')

START_DATE = '2022-03-21'
END_DATE = '2022-03-23'
LOCAL_STORAGE_PATH = 'ouraData{}to{}.csv'.format(START_DATE, END_DATE)

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


@application.route('/callback')
def callback():
    #old URL: http://localhost:8080/callback
    """Callback page
    Get the acces_token from response url from Oura. 
    Redirect to the sleep data page.
    """
    oura_session = OAuth2Session(OURA_CLIENT_ID, state=session['oauth_state'])
    session['oauth'] = oura_session.fetch_token(
                        OURA_TOKEN_URL,
                        client_secret=OURA_CLIENT_SECRET,
                        authorization_response=request.url)
    return redirect(url_for('.heartrate'))
                            #.sleep


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

    # #use panda to make result.json into oura-data.csv
    # df = pd.read_json('result.json')
    # df.to_csv('oura-data.csv')

    return "<h1>Nice</h1>"

#Riley
@application.route('/rileyapp')
def rileyapp():
    rurl =    "https://o558y4fmv4.execute-api.us-east-1.amazonaws.com/Testing/predict"
 
    payload = "{\r\n    \"payload\":\"12974,39,503,183.74,75,80,25.099\"\r\n}"
    headers = {
    'Content-Type': 'text/plain'
    }
 
    response = requests.request("POST", rurl, headers=headers, data=payload)
 
    print(response.text)
    return "<h1>Nice Riley</h1>"


    
#home page
@application.route('/')
def home():
    return "<h1>Welcome to your Oura application</h1>"

if __name__ == "__main__":

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    application.secret_key = os.urandom(24)
    #application.run(debug=False, host='127.0.0.1', port=8080)
    serve(application, host='0.0.0.0', port=80)
                                        #port=8080












#https://cloud.ouraring.com/v2/usercollection/heartrate
#https://api.ouraring.com/v1/sleep?
#https://api.ouraring.com/v1/heartrate?


#------------Old code to retreive Oura API v1 data----------------------
# @application.route('/sleep')
# def sleep():
#     """Sleep data page
#     Get sleep data from the OURA API
#     transform sleep data to a pandas DataFrame
#     store sleep data as a csv
#     return description of the DataFrame
#     """
#     oauth_token = session['oauth']['access_token']

#     sleep_data = requests.get('https://api.ouraring.com/v1/heartrate?'
#                               'start={}&end={}&access_token={}'
#                               .format(START_DATE, END_DATE, oauth_token))
#     json_sleep = sleep_data.json()
#     df = pd.DataFrame(json_sleep['sleep'])
#     df.to_csv(LOCAL_STORAGE_PATH)
#     return '<p>Successfully stored sleep data</p><p>{}</p>'\
#         .format(df.describe())