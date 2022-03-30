from flask import Flask, request, render_template, jsonify
import google.auth
import configparser

from googleapiclient.discovery import build

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')


def read_from_google_sheet(doc_id: str, range: str):
    credentials, _ = google.auth.default(
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    sheets_service = build('sheets', 'v4', credentials=credentials)
    sheet = sheets_service.spreadsheets()
    results = sheet.values().get(
        spreadsheetId=doc_id,
        range=range).execute()
    return results.get('values')


def return_tlds(lst):
    tlds = [tld[0].split('.')[-1] for tld in lst]
    return list(set(tlds))


def return_results(lst, tld: str, category: str):
    results = [result[0] for result in lst if tld in result[0] and category == result[1]]
    return list(set(results))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/tool/1', methods=['GET', 'POST'])
def tool_1():

    if request.method == 'POST':
        values = read_from_google_sheet(config['GOOGLE_SHEET']['ID'], 'data!A:D')
        results = return_results(values, request.form['tld'], request.form['category'])
        return render_template('results.html', results=results)
    
    elif request.method == 'GET':
        categories = read_from_google_sheet(config['GOOGLE_SHEET']['ID'], 'cat!A:A')
        categories = [x[0] for x in categories]
        tlds = read_from_google_sheet(config['GOOGLE_SHEET']['ID'], 'data!A:A')
        tlds = return_tlds(tlds[1:])
        return render_template('t1.html', tlds=tlds, categories=categories)


if __name__ == '__main__':
    app.run()
