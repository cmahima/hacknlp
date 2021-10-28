import numpy as np
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import secrets
from flask_cors import CORS
import spacy
import textwrap
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import requests

from spacy import displacy
from flaskext.markdown import Markdown

punctuation += '\n'
stopwords = list(STOP_WORDS)
spacy.cli.download("en_core_web_sm")


secret = secrets.token_urlsafe(32)
app = Flask(__name__)
CORS(app)
Markdown(app)
app.secret_key = secret


@app.route('/classify/',methods=['POST'])
def classify():


    # {'patients': [{
    #     'patient_id':123,
    #     'text':'test'
    # }]
    # 'type_of_classification': 'smoke'
    # }
    print("data is " + format(request.get_json()))
    data = request.get_json()
    patients = data['patients']
    type_of_classification = data['type_of_classification']

    smoke_parameters = {"candidate_labels": "SMOKER, NON SMOKER", "multi_label": False}
    alcohol_parameters = {"candidate_labels": "Alcoholic, NON Alcoholic", "multi_label": False}
    results = []

    for patient in patients:
        if type_of_classification == 'smoke':
            parameters = smoke_parameters
            label = 'SMOKER'
        else:
            parameters = alcohol_parameters
            label = 'Alcoholic'
        params = {
            "inputs" : patient['text'],
            "parameters": parameters,
        }
        response = requests.post('https://api-inference.huggingface.co/models/facebook/bart-large-mnli',
                                 json=params)

        scores = response.json()
        label_dict ={}
        for x,y in zip(scores['labels'],scores['scores']):
            print(x,y)
            label_dict[x] = y

        out_data = {
            'patient_id':patient['patient_id'],
            'score':label_dict[label],

        }
        results.append(out_data)

    output_data = {"data":results}

    return jsonify(output_data)

@app.route('/summarize/', methods=['POST'])
def summarize():
    text = request.get_json()['text']

    nlp_pl = spacy.load('en_core_web_sm')  # process original text according with the Spacy nlp pipeline for english
    document = nlp_pl(text)  # doc object

    tokens = [token.text for token in document]  # tokenized text
    reduction_rate = 0.2
    word_frequencies = {}
    for word in document:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    #print(max_frequency)

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    #print(word_frequencies)

    sentence_tokens = [sent for sent in document.sents]

    def get_sentence_scores(sentence_tok, len_norm=True):
        sentence_scores = {}
        for sent in sentence_tok:
            word_count = 0
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    word_count += 1
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]
            if len_norm:
                try:
                    sentence_scores[sent] = sentence_scores[sent] / word_count
                except:
                    pass
        return sentence_scores

    sentence_scores = get_sentence_scores(sentence_tokens,
                                          len_norm=False)  # sentence scoring without lenght normalization
    sentence_scores_rel = get_sentence_scores(sentence_tokens, len_norm=True)

    def get_summary(sentence_sc, rate):
        summary_length = int(len(sentence_sc) * rate)
        summary = nlargest(summary_length, sentence_sc, key=sentence_sc.get)
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        return summary

    #print("- NON_REL: " + get_summary(sentence_scores, reduction_rate))
    #print("- REL: " + get_summary(sentence_scores_rel, reduction_rate))
    return jsonify({'result': get_summary(sentence_scores, reduction_rate)})


@app.route('/ner/', methods=['POST'])
def extract_entities():
    text = request.get_json()['text']
    nlp_pl = spacy.load('en_ner_bc5cdr_md')  # process original text according with the Spacy nlp pipeline for english
    #nlp_pl = spacy.load('en_core_sci_md')
    #nlp_pl.add_pipe('negex')
    document = nlp_pl(text)

    def get_entity_options():
        entities = ["DISEASE", "CHEMICAL", "NEG_ENTITY"]
        colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)',
                  'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)',
                  "NEG_ENTITY": 'linear-gradient(90deg, #ffff66, #ff6600)'}
        options = {"ents": entities, "colors": colors}
        return options

    options = get_entity_options()
    result = displacy.render(document, style = 'ent', options=options)

    return jsonify({'result':result})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8000)
