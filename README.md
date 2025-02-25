# Trans Informed server

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/beawitcht/transinformed-server.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/beawitcht/transinformed-server/context:python) ![LGTM Grade](https://img.shields.io/lgtm/grade/javascript/github/beawitcht/transinformed-server) ![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/www.transinformed.co.uk?publish) [![Twitter Follow](https://img.shields.io/twitter/follow/beawitcht?style=social)](https://www.twitter.com/beawitcht)
***

<p align="center">
    <img src="https://raw.githubusercontent.com/beawitcht/transinformed-server/main/app/static/images/logo.svg" width="200" alt="Trans Informed logo">
</p>

## About
#### ***This service is still an early prototype.***
This is a web app to generate contextualised documents for people to bring to their GPs to provide them with one document containing the most important information for both the GP and the patient.


## Setup guide

### Installation

#### Navigate to app directory:
```bash
cd app/
```
#### Install with pip:

```bash
pip install -r requirements.txt
```
### Configure .env
#### The following environment variables are required:
```
PDF_API_KEY=<your-pdf-api-key> # api key for conversion to PDF: convertapi.com
RECAPTCHA_PUBLIC_KEY=<your-recaptcha-public-key> # google recaptcha public key
RECAPTCHA_PRIVATE_KEY=<your-recaptcha-private-key> # google recaptcha private key
IS_DEV = 1 # set to 1 to disable caching
```
### Run with gunicorn
```bash
gunicorn -w 4 -b 127.0.0.1:8000 main:app
```
***
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T7BLO3U)
