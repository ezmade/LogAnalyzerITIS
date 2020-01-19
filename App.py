from flask import Flask, render_template, request
from sqlite3 import connect
import json
from datetime import datetime
import operator

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/reportByCountries', methods=['GET'])
def reportByCountries():
    connection = connect('data.db')
    cursor = connection.cursor()
    req = cursor.execute('SELECT country FROM requests WHERE NOT country="None";')
    countries = [country[0] for country in req]
    connection.close()
    countriesDict = dict()
    for country in countries:
        if country in countriesDict:
            countriesDict[country] += 1
        else:
            countriesDict[country] = 1
    countriesList = sorted(countriesDict.items(), key=operator.itemgetter(1), reverse=True)
    return json.dumps(countriesList)
    

@app.route('/reportByCountriesAndCategory', methods=['POST'])
def reportByCountriesAndCategory():
    connection = connect('data.db')
    cursor = connection.cursor()
    category = request.data.decode('UTF-8')
    req = cursor.execute('SELECT country FROM requests WHERE NOT country="None" AND category="%s";' % category)
    countries = [country[0] for country in req]
    connection.close()
    countriesDict = dict()
    for country in countries:
        if country in countriesDict:
            countriesDict[country] += 1
        else:
            countriesDict[country] = 1
    countriesList = sorted(countriesDict.items(), key=operator.itemgetter(1), reverse=True)
    return json.dumps(countriesList)


@app.route('/reportByTimeAndCategory', methods=['POST'])
def reportByTimeAndCategory():
    connection = connect('data.db')
    cursor = connection.cursor()
    category = request.data.decode('UTF-8')
    req = cursor.execute('SELECT time FROM requests WHERE category="%s";' % category)
    times = [datetime.strptime(record[0], '%H:%M:%S') for record in req]
    connection.close()
    dayPart = {'NIGHT': 0, 'MORNING': 0, 'DAY': 0, 'EVENING': 0}
    for t in times:
        if (t.hour < 6) and (t.hour >= 0):
            dayPart['NIGHT'] += 1
        elif (t.hour < 12):
            dayPart['MORNING'] += 1
        elif (t.hour < 18):
            dayPart['DAY'] += 1
        else:
            dayPart['EVENING'] += 1
    return json.dumps(dayPart) 


if __name__ == '__main__':
    app.run()