from . import db, DB_DATA
from flask import Blueprint, render_template, request, flash, redirect, url_for
import pygal
from pygal.style import Style, RedBlueStyle

views = Blueprint('views', __name__)

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
        vehicle2 = vehicle

        if vehicle == 'Car':
            vehicle = 'CAR'
        elif vehicle == 'Bus':
            vehicle = 'BUS'
        elif vehicle == 'Van':
            vehicle = 'VAN'
        elif vehicle == 'Taxi':
            vehicle = 'TAXI'
        elif vehicle == 'Truck':
            vehicle = 'TRUCK'
        elif vehicle == 'Motorcycle':
            vehicle = 'MOTORCYCLE'
        elif vehicle == 'Delivery Van':
            vehicle = 'DELIVERYVAN'
        elif vehicle == 'Jeep':
            vehicle = 'PUJ'
        elif vehicle == 'Closed Van':
            vehicle = 'CLOSEDVAN'
        elif vehicle == 'Wing Van':
            vehicle = 'WINGVAN'
        elif vehicle == 'Pickup':
            vehicle = 'PICKUP'
        elif vehicle == 'Dump Truck':
            vehicle = 'DUMPTRUCK'
        elif vehicle == 'Elf Truck':
            vehicle = 'ELFTRUCK'
        elif vehicle == 'UV Express':
            vehicle = 'UVEXPRESS'
        elif vehicle == 'Trailer Truck':
            vehicle = 'TRAILERTRUCK'
        elif vehicle == 'Armored Van':
            vehicle = 'ARMOREDVAN'

        if city == 'Metro Manila':
            query1 = db.engine.execute(f'''
                                       SELECT i.longitude, i.latitude, i.date
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}';
                                       ''').fetchall()
        else:
            query1 = db.engine.execute(f'''
                                       SELECT i.longitude, i.latitude, i.date, i.city
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}' and i.city = '{city}';
                                       ''').fetchall()
        longs = []
        lats = []
        for row in query1:
            if '2020' in row.date:
                longs.append(row.longitude)
                lats.append(row.latitude)

        if city == 'Metro Manila':
            query2 = db.engine.execute(f'''
                                       SELECT i.location, i.date, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}'
                                       GROUP BY i.location ORDER BY COUNT(*) DESC LIMIT 15;
                                       ''').fetchall()
        else:
            query2 = db.engine.execute(f'''
                                       SELECT i.location, i.date, i.city, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}' and i.city = '{city}'
                                       GROUP BY i.location ORDER BY COUNT(*) DESC LIMIT 15;
                                       ''').fetchall()
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

        if city == 'Metro Manila':
            query3 = db.engine.execute(f'''
                                       SELECT i.id, i.date, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}'
                                       GROUP BY i.date
                                       ORDER BY i.date;
                                       ''').fetchall()
        else:
            query3 = db.engine.execute(f'''
                                       SELECT i.id, i.date, i.city, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}' and i.city = '{city}'
                                       GROUP BY i.date
                                       ORDER BY i.date;
                                       ''').fetchall()
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

        if city == 'Metro Manila':
            query4 = db.engine.execute(f'''
                                       SELECT i.direction, i.date, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}'
                                       GROUP BY i.direction;
                                       ''').fetchall()
        else:
            query4 = db.engine.execute(f'''
                                       SELECT i.direction, i.date, i.city, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE v.vehicle = '{vehicle}' and i.city = '{city}'
                                       GROUP BY i.direction;
                                       ''').fetchall()

        chart4 = pygal.Pie()
        for row in query4:
            if '2020' in row.date:
                chart4.add(row.direction, row.count)
        chart4_data = chart4.render_data_uri()

        if city == 'Metro Manila':
            query5 = db.engine.execute('''
                                       SELECT v.vehicle, i.date, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       GROUP BY v.vehicle ORDER BY COUNT(*) DESC LIMIT 30;
                                       ''').fetchall()
        else:
            query5 = db.engine.execute(f'''
                                       SELECT v.vehicle, i.date, i.city, COUNT(*) as count
                                       FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                                       WHERE i.city = '{city}'
                                       GROUP BY v.vehicle ORDER BY COUNT(*) DESC LIMIT 30;
                                       ''').fetchall()
        chart5 = pygal.Treemap(legend_at_bottom=True)
        for row in query5:
            if '2020' in row.date:
                chart5.add(row.vehicle, row.count)
        chart5_data = chart5.render_data_uri()

        return render_template('main.html', city=city, vehicle=vehicle2, longs=longs, lats=lats, chart2_data=chart2_data, chart3_data=chart3_data, chart4_data=chart4_data, chart5_data=chart5_data)

    query1 = db.engine.execute('''
                               SELECT i.longitude, i.latitude, i.date
                               FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                               WHERE v.vehicle = 'CAR';
                               ''').fetchall()
    longs = []
    lats = []
    for row in query1:
        if '2020' in row.date:
            longs.append(row.longitude)
            lats.append(row.latitude)

    query2 = db.engine.execute('''
                               SELECT i.location, i.date, COUNT(*) as count
                               FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                               WHERE v.vehicle = 'CAR'
                               GROUP BY i.location ORDER BY COUNT(*) DESC LIMIT 15;
                               ''').fetchall()
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

    query3 = db.engine.execute('''
                               SELECT i.id, i.date, COUNT(*) as count
                               FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                               WHERE v.vehicle = 'CAR'
                               GROUP BY i.date
                               ORDER BY i.date;
                               ''').fetchall()
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

    query4 = db.engine.execute('''
                               SELECT i.direction, i.date, COUNT(*) as count
                               FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                               WHERE v.vehicle = 'CAR'
                               GROUP BY i.direction;
                               ''').fetchall()
    chart4 = pygal.Pie()
    for row in query4:
        if '2020' in row.date:
            chart4.add(row.direction, row.count)
    chart4_data = chart4.render_data_uri()

    query5 = db.engine.execute('''
                               SELECT v.vehicle, i.date, COUNT(*) as count
                               FROM incident i JOIN incident_vehicles v ON i.id = v.incident_id
                               GROUP BY v.vehicle ORDER BY COUNT(*) DESC LIMIT 30;
                               ''').fetchall()
    chart5 = pygal.Treemap(legend_at_bottom=True)
    for row in query5:
        if '2020' in row.date:
            chart5.add(row.vehicle, row.count)
    chart5_data = chart5.render_data_uri()

    return render_template('main.html', city='Metro Manila', vehicle='Car', longs=longs, lats=lats, chart2_data=chart2_data, chart3_data=chart3_data, chart4_data=chart4_data, chart5_data=chart5_data)