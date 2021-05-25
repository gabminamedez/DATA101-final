from . import db, DB_DATA
from flask import Blueprint, render_template, request, flash, redirect, url_for
import pygal
from pygal.style import Style, RedBlueStyle

views = Blueprint('views', __name__)

ACCESS_KEY = 'pk.eyJ1IjoiZ2FibWluYW1lZGV6IiwiYSI6ImNrb2F6eGRtODBnMGQycG83amRldTR1cGsifQ.nAVNKTR9tYX6JpaUKRc0LA'

# Route will begin with initial sentence for data filtering
@views.route('/', methods=['GET', 'POST'])
def main():
    '''
    This route loads main.html 
    - Request for user to input from sentence fill.
    '''
    DB_DATA.incident().to_sql(name='incident', if_exists='replace', con=db.engine, index=False)         #change if_exists to replace when resetting database to default
    DB_DATA.vehicle().to_sql(name='incident_vehicles', if_exists='replace', con=db.engine, index=False) #change if_exists to replace when resetting database to default
    DB_DATA.tweet().to_sql(name='incident_tweet', if_exists='replace', con=db.engine, index=False)      #change if_exists to replace when resetting database to default

    if request.method == 'POST':
        city = request.form.get('city')
        vehicle = request.form.get('vehicle')

        if city == '':
            flash('City must be inputted to continue', category='error')
        elif vehicle == '':
            flash('Vehicle must be inputted to continue', category='error')

        return render_template('main.html', city=city, vehicle=vehicle)

    query1 = db.engine.execute('SELECT longitude, latitude, date FROM incident;').fetchall()
    longs = []
    lats = []
    for row in query1:
        if '2020' in row.date:
            longs.append(row.longitude)
            lats.append(row.latitude)

    query2 = db.engine.execute('SELECT location, date, COUNT(*) as count FROM incident GROUP BY location ORDER BY COUNT(*) DESC LIMIT 15;').fetchall()
    chart2 = pygal.HorizontalBar(style=RedBlueStyle)
    chart2.show_legend = False
    locations = []
    counts = []
    query2 = reversed(query2)
    for row in query2:
        if '2020' in row.date:
            locations.append(row.location)
            counts.append(row.count)
    chart2.x_labels = tuple(locations)
    chart2.add('', counts)
    chart2_data = chart2.render_data_uri()

    from datetime import datetime, timedelta
    query3 = db.engine.execute('SELECT id, date, COUNT(*) as count FROM incident GROUP BY date ORDER BY date;').fetchall()
    chart3 = pygal.Line(x_label_rotation=45)
    dates = []
    counts = []
    isComplete = [False, False, False, False, False, False]
    for row in query3:
        if '2020' in row.date:
            if '2020-01' in row.date and isComplete[0] == False:
                dates.append(row.date)
                isComplete[0] = True
            elif '2020-03' in row.date and isComplete[1] == False:
                dates.append(row.date)
                isComplete[1] = True
            elif '2020-05' in row.date and isComplete[2] == False:
                dates.append(row.date)
                isComplete[2] = True
            elif '2020-07' in row.date and isComplete[3] == False:
                dates.append(row.date)
                isComplete[3] = True
            elif '2020-09' in row.date and isComplete[4] == False:
                dates.append(row.date)
                isComplete[4] = True
            elif '2020-11' in row.date and isComplete[5] == False:
                dates.append(row.date)
                isComplete[5] = True
            else:
                dates.append('')

            counts.append(row.count)
    chart3.x_labels = dates
    chart3.add('', counts)
    chart3.show_legend = False
    chart3_data = chart3.render_data_uri()

    query4 = db.engine.execute('SELECT direction, date, COUNT(*) as count FROM incident GROUP BY direction;').fetchall()
    chart4 = pygal.Pie()
    for row in query4:
        if '2020' in row.date:
            chart4.add(row.direction, row.count)
    chart4_data = chart4.render_data_uri()

    return render_template('main.html', city='metro', vehicle='car', longs=longs, lats=lats, chart2_data=chart2_data, chart3_data=chart3_data, chart4_data=chart4_data)