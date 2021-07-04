import logging
import json
from datetime import datetime
from textblob import TextBlob
import nltk.data
import os
import azure.functions as func

# nltk.data.path.append(os.path.join(os.path.curdir, 'nltk_data'))
french_tokenizer = nltk.data.load(os.path.join(os.path.curdir,'nltk_data/tokenizers/punkt/french.pickle'))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        text: str = req_body['text']
    except ValueError:
        pass
    else:        
        blob: TextBlob = TextBlob(text, tokenizer=french_tokenizer)
        polarity = blob.sentiment.polarity

        if polarity:
            timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = { "timestamp" : timestamp, "text": text, "polarity": polarity }
            return func.HttpResponse(json.dumps(response), mimetype='application/json')
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a tet in the query string or in the request body for a sentiment analysis response.",
                status_code=400
            )
