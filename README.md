# YT-cloud
> v0.1.0
<!-- -->
Currently supporting a basic command line tool to upload videos to youtube using the Youtube V3 API. Due to the intended purposes of the code, videos are uploaded as private and the description cannot be changed. For a more robust command line tool of this kind see [youtube-upload](https://github.com/tokland/youtube-upload).

### Contents
- [Setup and Dependencies](README.md#setup-and-dependencies)
- [Usage](README.md#usage)

## Setup and Dependencies
### Setup
A client secret must be obtained from [Google Cloud](https://cloud.google.com/gcp?utm_source=google&utm_medium=cpc&utm_campaign=na-US-all-en-dr-bkws-all-all-trial-b-dr-1605212&utm_content=text-ad-none-any-DEV_c-CRE_665735450768-ADGP_Hybrid+%7C+BKWS+-+BRO+%7C+Txt_GCP-KWID_43700077212154724-kwd-14471151&utm_term=KW_gcp-ST_gcp&gad_source=1&gclid=Cj0KCQiAkKqsBhC3ARIsAEEjuJixvNK9mqeyrloUhchY_YVI0mTSPLnN7STP9Fl3awsIwAYJyyin8DgaAg8uEALw_wcB&gclsrc=aw.ds&hl=en) to use Youtube API services. Once you have created an account, navigate to your cloud console. Find the APIs and Services Library. Enable the Youtube Data API V3.
![image](https://github.com/Colby-Coffman/YT-cloud/assets/114829458/e18fdd69-4219-4931-bd40-814f8bde818e)
<!-- -->
Once the service has been enabled, navigate to your Credentials page. Click Create Credentials, then OAuth client id.
![image](https://github.com/Colby-Coffman/YT-cloud/assets/114829458/836810f7-75bb-448a-ae85-9aaf95e865f9)
<!-- -->
Select Desktop app as the application type, then create the client id. Download the client secret json and place it in the source code directory. It is not required to keep the secrets file in this directory, but it spares you having to pass it as an argument.

All dependencies can be downloaded using pip
### Dependencies
- Has been only tested for Python 3.10. Earlier versions may be compatible
- [Google API Client](https://github.com/googleapis/google-api-python-client)
- [Google Auth](https://github.com/googleapis/google-auth-library-python/tree/main)
- [Google Oauthlib Integration](https://github.com/googleapis/google-auth-library-python-oauthlib)
	- May be replaced at a future date
- [PyQt5](https://pypi.org/project/PyQt5/)
	- Not a required import if run solely through the command line
	- Likely compatible with other Qt versions, will fix at a later date.
 ## Usage
Upon first execution, a URL will appear in your browser for Oauth2 authorization. The requested scopes are listed in auth.py. Upon authorization your client credentials is placed in the source directory. Keep this file secure.
 ```
python main.py [--file=RELATIVE/ABSOLUTE PATH] [--clientcredentials=RELATIVE/ABSOLUTE PATH]
[--clientsecret=RELATIVE/ABSOLUTE PATH] [--interactive] [--chunksize=INTEGER]
```
Pass a video as an argument using either an absolute or relative path to the current working directory. You can pass a different client credentials or client secret file using --clientcredentials or --clientsecret, but the program will use the files in the source directory by default. Use the --interactive flag to pick a video/secret/credentials file using the PyQt file picker. You can pass an integer to the --chunksize flag to direct the upload rate in bytes. For smaller files you can attempt to upload all at once by passing a -1 to this argument. The maximum chunksize google allows is 5 MB. The program defaults to 4 MiB.

If the access type is changed in main.py, YouTube will still restrict videos uploaded using this script as private. In order to make this script upload videos as public, you need to verify with google.

Additionally, you are restricted to 6 uploads per day. more can be obtained once you are certified.
