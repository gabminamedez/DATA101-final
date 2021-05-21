from . import db,DB_DATA
from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

# Route will begin with initial sentence for data filtering
@views.route('/')
def main():
    '''
    This route loads main.html 
    - Request for user to input from sentence fill.
    '''
    DB_DATA.incident().to_sql(name='incident',if_exists='replace', con=db.engine, index=False)
    DB_DATA.vehicle().to_sql(name='incident_vehicles',if_exists='replace', con=db.engine, index=False)
    DB_DATA.tweet().to_sql(name='incident_tweet', con=db.engine,if_exists='replace', index=False)
    if request.method == 'POST':
        city = request.form.get('city')
        vehicle = request.form.get('vehicle')

        if city == '':
            flash('City must be inputted to continue', category='error')
        elif vehicle == '':
            flash('Vehicle must be inputted to continue', category='error')
    return render_template('main.html')