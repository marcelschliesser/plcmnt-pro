# plcmnt-pro
Read data from a Google Sheet and present it via a Flask App to the end user.

## Create Service Account JSON
```
gcloud iam service-accounts keys create key.json --iam-account=118210456628-compute@developer.gserviceaccount.com
gcloud iam service-accounts disable 118210456628-compute@developer.gserviceaccount.com
gcloud iam service-accounts enable 118210456628-compute@developer.gserviceaccount.com
```
```
set GOOGLE_APPLICATION_CREDENTIALS="key.json"
```

## Deploy
```
gcloud run deploy first-try --region=europe-west3 --source .
```

## B64 Encode
```
certutil -encode robots.txt tmp.b64 && findstr /v /c:- tmp.b64 > data.b64
```