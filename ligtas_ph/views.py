from . import db, DB_DATA
from flask import Blueprint, render_template, request, flash, redirect, url_for

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
    DB_DATA.tweet().to_sql(name='incident_tweet', con=db.engine, if_exists='replace', index=False)      #change if_exists to replace when resetting database to default
    if request.method == 'POST':
        city = request.form.get('city')
        vehicle = request.form.get('vehicle')

        if city == '':
            flash('City must be inputted to continue', category='error')
        elif vehicle == '':
            flash('Vehicle must be inputted to continue', category='error')

        # return redirect(url_for('views.results'))

        return render_template('main.html', city=city, vehicle=vehicle)

    return render_template('main.html')