# 2021_11_25 - Serverless WebApp using GoogleAppEngine

Based on the quickstart example https://cloud.google.com/appengine/docs/standard/python3/building-app

Google Slides Presentation: https://docs.google.com/presentation/d/e/2PACX-1vS4SdF2XM9-mip0_WvLNEFAYCObsZW6O1iZvWboT_sfx2I_jU1zJoMSyh_4Mfk0UhNymuf3It4mRW5-/pub?start=false&loop=false&delayms=3000

## Windows

### Requirements

* Install `git`
* Install `python`
* Install `virtualenvwrapper`
* Install Google Cloud SDK https://cloud.google.com/sdk/docs/install
* Create a project in Gcloud https://console.cloud.google.com/


### Steps

0. Clone the repo with `git clone git@github.com:vperezb/python-meetups.git`
0. Create a virtualenv `mkvirtualenv venv`
0. Navigate to the `/python-meetups/2021_11_25_pybcn_meetup` folder
0. Install app requirements `pip install -r requirements.txt`
0. Download new `.json` credentials from `Service Accounts` sections in https://console.cloud.google.com/apis/credentials
0. Set credentials for the environment `set GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json`
0. In the same dir, run `python main.py`

### Deploy

* gcloud init
* gcloud projects list
* gcloud config set project my-project-1470411376725
* gcloud app deploy app.yaml
