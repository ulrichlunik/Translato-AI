from flask import Flask, request, url_for, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['post'])
def index_post():
    text_To_Translate = request.form['text']
    language = request.form['language']
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = 'translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{ 'text': text_To_Translate }]

    try:

        # Make the call using post
        translator_request = requests.post(constructed_url, headers=headers, json=body)
        # Retrieve the JSON response
        print(translator_request)
        translator_response = translator_request.json()
        # Retrieve the translation
        translated_text = translator_response[0]['translations'][0]['text']

        # Call render template, passing the translated text,
        # original text, and target language to the template
        return render_template(
            'results.html',
            translated_text=translated_text,
            original_text=text_To_Translate,
            target_language=language
        )
    except Exception as e:
        print('exception')
        print('error: ',e)
        # print('type ',type(e))    # the exception type
        # print(e.args)     # arguments stored in .args
        # print(e)  
        

