import csv
from flask import Flask, request, render_template, jsonify
import google.auth
import configparser

from googleapiclient.discovery import build

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

config = configparser.ConfigParser()
config.read('config.ini')


def google_sheet_service():
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    sheets_service = build('sheets', 'v4', credentials=credentials)
    return sheets_service


def return_tlds(lst):
    tlds = [tld[0].split('.')[-1] for tld in lst]
    return list(set(tlds))



def return_topics(lst):
    topics1 = [topic[1] for topic in lst if topic[1] != 'null']
    topics2 = [topic[2] for topic in lst if topic[2] != 'null']
    return list(set(topics1)), list(set(topics2))


def return_results(lst, tld: str, category: str):
    results = [result[0] for result in lst if tld in result[0] and category == result[1]]
    return list(set(results))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    sheet_service = google_sheet_service()
    sheet = sheet_service.spreadsheets()
    results = sheet.values().get(spreadsheetId=config['GOOGLE_SHEET']['ID'],
                                 range=config['GOOGLE_SHEET']['RANGE']).execute()
    values = results.get('values', [])[1:]
    return jsonify([{'domain': t[0], 'cat1': t[1], 'cat2': t[2], 'cat3': t[3]} for t in values])

@app.route('/t1', methods=['GET', 'POST'])
def t1():
    sheet_service = google_sheet_service()
    sheet = sheet_service.spreadsheets()
    results = sheet.values().get(spreadsheetId=config['GOOGLE_SHEET']['ID'],
                                range=config['GOOGLE_SHEET']['RANGE']).execute()
    values = results.get('values', [])[1:]
    if request.method == 'POST':
        results = return_results(values, request.form['tld'], request.form['topic'])
        return render_template('results.html', results=results)
    elif request.method == 'GET':
        tlds = return_tlds(values)
        topics1, topics2 = return_topics(values)
        return render_template('t1.html', tlds=tlds, topics1=topics1, topics2=topics2)


if __name__ == '__main__':
    app.run()
