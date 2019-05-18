from flask import url_for, request, render_template, redirect
from app import app
from modules.adt import Earthquakes
import datetime

DATE = 0

@app.route("/")
def hello():
    return render_template('beggining.html')


@app.route("/map/date", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('get_year.html')
    elif request.method == 'POST':
        date = request.form['date']
        return redirect(url_for('get_map', date=date))
    else:
        return "<h2>Invalid request</h2>"


@app.route('/date/<date>', methods=['GET', 'POST'])
def get_map(date):
    """
    renders a map of date that user write on site.
    :param date:
    :return:
    """
    map_name = checker(date, map_true=True)
    try:
        render_template(map_name)
    except:
        Earthquakes(date).run()
    return render_template(map_name)

@app.route("/text/date", methods=['GET', 'POST'])
def create1():
    if request.method == 'GET':
        return render_template('get_year.html')
    elif request.method == 'POST':
        date = request.form['date']
        return redirect(url_for('get_text', date=date))
    else:
        return "<h2>Invalid request</h2>"

@app.route('/text/<date>', methods=['GET', 'POST'])
def get_text(date):
    text_name = checker(date, text_true=True)
    try:
        render_template(text_name)
    except:
        Earthquakes(date).run_text()
    return render_template(text_name)

@app.route('/prediction', methods=['GET', 'POST'])
def get_prediction():
    global DATE
    if DATE != datetime.datetime.now().date():
        Earthquakes(1991).get_prediction()
        DATE = datetime.datetime.now().date()
    return render_template('Map_prediction.html')

@app.route('/about')
def about():
    return render_template('about.html')

def checker(date, map_true=False, text_true=False):
    if request.method == 'GET' or request.method == 'POST':
        date = date.split('.')
        try:
            date1 = str(datetime.datetime.now().date()).split('-')
            a = date1[-3]
            b = date1[-2]
            c = date1[-1]
            if len(date) > 3:
                raise ValueError
            date[-1] = int(date[-1])
            if len(date) >= 2:
                date[-2] = int(date[-2])
            if len(date) >= 3:
                date[-3] = int(date[-3])
            if not(1900 <date[-1] <= int(a)):
                raise ValueError
            elif len(date) >= 2 and date[-1] == a and not(0 < date[-2] < date1[-2]):
                raise ValueError

            elif  len(date) >= 2 and not(0< date[-2] < 13):
                    raise ValueError
            if  len(date) >= 2 and int(date[0]) in [1, 3, 5, 7, 8, 10, 12] and not(0< date[-2] < 32):
                raise ValueError

            elif len(date) >= 2 and int(date[0]) in [4, 6, 9, 11] and not(0< date[-2] < 31):
                raise ValueError
            elif len(date) == 3 and int(date[0]) == 2 and not(0< date[-2] < 29):
                raise ValueError
        except ValueError:
            return render_template('Incorrect.html')

        if map_true:
            map_name = "Map_" + str(int(date[0]))
            if len(date) >= 2:
                map_name += '_' + str(int(date[1]))
            if len(date) == 3:
                map_name += "_" + str(int(date[2]))
            map_name += '.html'
            return map_name
        if text_true:
            text_name = "Text_" + str(int(date[0]))
            if len(date) >= 2:
                text_name += '_' + str(int(date[1]))
            if len(date) == 3:
                text_name += "_" + str(int(date[2]))
            text_name += '.html'
            return text_name

