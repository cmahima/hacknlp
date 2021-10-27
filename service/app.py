import numpy as np
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import secrets
from flask_cors import CORS
import spacy
import textwrap
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
punctuation += '\n'
stopwords = list(STOP_WORDS)
spacy.cli.download("en_core_web_sm")


secret = secrets.token_urlsafe(32)
app = Flask(__name__)
CORS(app)
app.secret_key = secret


@app.route('/summarize/', methods=['POST'])
def summarize():
    text = '''The patient was brought to the operating room and placed in the supine position. Adequate general endotracheal anesthesia was induced. Appropriate monitoring devices were placed. The chest, abdomen and legs were prepped and draped in the sterile fashion. The right greater saphenous vein was harvested and prepared by ligating all branches with 4-0 Surgilon and flushed with heparinized blood. Hemostasis was achieved in the legs and closed with running 2-0 Dexon in the subcutaneous tissue and running 3-0 Dexon subcuticular in the skin. Median sternotomy incision was made and the left mammary artery was dissected free from its takeoff of the subclavian to its bifurcation at the diaphragm and surrounded with papaverine-soaked gauze. The pericardium was opened. The pericardial cradle was created. The patient was fully heparinized and cannulated with a single aortic and single venous cannula and bypass was instituted. A retrograde cardioplegic cannula was placed with a pursestring suture of 4-0 Prolene suture in the right atrial wall into the coronary sinus and tied to a Rumel tourniquet. An antegrade cardioplegic needle sump combination was placed in the ascending aorta and tied in place with 4-0 Prolene. The ascending aorta was crossclamped. Cold blood potassium cardioplegia was given to the ascending aorta followed by sumping through the ascending aorta followed by cold retrograde potassium cardioplegia. The obtuse marginal coronary artery was identified and opened and end-to-side anastomosis was performed to the reversed autogenous saphenous vein with running 7-0 Prolene suture and the vein was cut to length. Cold antegrade and retrograde cardioplegia were given and the posterior descending branch of the right coronary artery was identified and opened. End-to-side anastomosis was performed with a running 7-0 Prolene suture and the vein was cut to length. Cold antegrade and retrograde potassium cardioplegia were given. The mammary artery was clipped distally, divided and spatulated for anastomosis. The anterior descending was identified and opened. End-to-side anastomosis was performed through the left internal mammary artery with running 8-0 Prolene suture. The mammary pedicle was sutured to the heart with interrupted 5-0 Prolene suture. A warm antegrade and retrograde cardioplegia were given. The aortic crossclamp was removed. The partial occlusion clamp was placed. Aortotomies were made. The veins were cut to fit these and sutured in place with running 5-0 Prolene suture. A partial occlusion clamp was removed. All anastomoses were inspected and noted to be patent and dry. Ventricular and atrial pacing wires were placed. The patient was fully warmed and weaned from cardiopulmonary bypass. The patient was decannulated in the routine fashion and Protamine was given. Good hemostasis was noted. A single mediastinal and left pleural chest tube were placed. The sternum was closed with interrupted wire, linea alba with running 0 Prolene, the sternal fascia was closed with running 0 Prolene, the subcutaneous tissue with running 2-0 Dexon and the skin with running 3-0 Dexon subcuticular stitch. The patient tolerated the procedure well.
    '''
    nlp_pl = spacy.load('en_core_web_sm')  # process original text according with the Spacy nlp pipeline for english
    document = nlp_pl(text)  # doc object

    tokens = [token.text for token in document]  # tokenized text
    reduction_rate = 0.1
    word_frequencies = {}
    for word in document:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    print(max_frequency)

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    print(word_frequencies)

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

    print("- NON_REL: " + get_summary(sentence_scores, reduction_rate))
    print("- REL: " + get_summary(sentence_scores_rel, reduction_rate))
    return jsonify({'result': get_summary(sentence_scores, reduction_rate)})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8000)
