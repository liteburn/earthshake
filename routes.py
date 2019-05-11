from flask import Flask, url_for, request, render_template, redirect
from app import app
from adt import Earthquakes\

@app.route("/")
def hello():
    return render_template('beggining.html')


@app.route("/create", methods=['GET', 'POST'])
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
    if request.method == 'GET' or request.method == 'POST':
        date = date.split('.')
        map_name = "Map_" + str(int(date[0]))

        if len(date) >= 2:
            map_name += '_' + str(int(date[1]))
        if len(date) == 3:
            map_name += "_" + str(int(date[2]))
        map_name += '.html'
        print([map_name])
        Earthquakes(date)
        return render_template(map_name)
    else:
        return "<h2> Invalid request </h2>"
