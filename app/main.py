from flask import Flask, render_template, send_file, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from docproc.populate_doc import generate_document
from input_form import InputForm
from pathlib import Path
import requests
import os
import json


from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / '.env')

api_key = os.getenv('PDF_API_KEY')
is_dev = os.getenv('IS_DEV')
# configure app
app = Flask(__name__)
limiter = Limiter(
    app, 
    key_func=get_remote_address,
    storage_uri="memory://",
)
app.config['WTF_CSRF_ENABLED'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')



# disable caching if in development mode
if is_dev == '0':
    cache = Cache(app, config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': Path(__file__).resolve().parent / 'tmp' / 'cache', 'CACHE_SOURCE_CHECK': True })
else:
    cache = Cache(app, config={'CACHE_TYPE': 'NullCache'})

@app.after_request
def add_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    response.headers['Content-Security-Policy'] = f'default-src \'none\'; script-src \'self\' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; img-src \'self\' data:;  style-src \'self\'; font-src \'self\'; connect-src \'self\'; frame-src https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/;'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


@app.route("/", methods=['GET', 'POST'])
@limiter.limit("5 per day", exempt_when=lambda: request.method == 'GET' or request.form.get('docx'))
@cache.cached(timeout=60 * 60 * 24 * 7, unless=lambda: request.method == 'POST')
def home():
    api_data = json.loads(requests.get(f"https://v2.convertapi.com/user?Secret={api_key}").text)
    try:
        seconds_left = api_data['SecondsLeft']
    except KeyError:
        seconds_left = 0

    # check if api limit reached
    if int(seconds_left) < 10:
        pdf_available = False
    else:
        pdf_available = True

    form = InputForm()
    if form.validate_on_submit():
        if form.docx.data:
            filetype = "docx"
        elif form.pdf.data:
            filetype = "pdf"
        file = generate_document(form.data, filetype)

        try:
            return send_file(file, download_name=f"myhealthcareguide.{filetype}")
        except file.getvalue() is None:
            if filetype == "pdf":
                return ("PDF downloads maxxed please download .docx version")
            else:
                return ("An error occured, please try again later")

    return render_template("index.html", form=form, pdf_available=pdf_available)


@app.route("/about", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def about():
    return render_template("about.html")


@app.route("/resources", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def resources():
    return render_template("resources.html")

@app.route("/sources", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def sources():
    return render_template("sources.html")

if __name__ == '__main__':
    app.run()
