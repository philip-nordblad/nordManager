
from datetime import datetime, timedelta
from flask_login import login_required, login_user, current_user
from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)
from .forms import ShiftForm, DayAvailabilityForm, AvailabilityForm
from .models import Shift, User
from . import db






bp = Blueprint('schedule',__name__,url_prefix = '/schedule' )



#need a 




@bp.route('/add_availability', methods=['GET', 'POST'])
def add_availability():
    form = AvailabilityForm()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if form.validate_on_submit():
        print("Form submitted successfully!")
        # Process form data
        availability = {}
        availability["total_hours"] = form.total_hours.data
        for i, day in enumerate(days_of_week):
            if form.days[i].available.data:
                if form.days[i].all_day.data:
                    availability[day.lower()] = {'start': '00:00', 'end': '23:59'}
                else:
                    if form.days[i].start_time.data == None:
                        form.days[i].start_time.data = datetime.strptime('00:00:00', '%H:%M:%S').time()
                        
                    form.days[i].end_time.data = datetime.strptime('23:59:00', '%H:%M:%S').time()
                    availability[day.lower()] = {
                        'start': form.days[i].start_time.data.strftime('%H:%M'),
                        'end': form.days[i].end_time.data.strftime('%H:%M')
                    }
        
        

        print("User Availability:", availability)

        # need to insert availability 
        id = current_user.id
        user = User.query.filter_by(id=id).first()

        user.availability = availability
        db.session.commit()




    else:
        flash(f"Form failed: {form.errors}")
        
    return render_template('/schedule/availability.html', form=form, days_of_week=days_of_week)


    
def create_schedule():

    # need to get all availability forms
    

    # given multiple forms submitted

    
    #availability_forms

    pass    