
from datetime import datetime, timedelta
from flask_login import login_required, login_user
from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)
from .forms import ShiftForm, DayAvailabilityForm, AvailabilityForm





bp = Blueprint('schedule',__name__,url_prefix = '/schedule' )



@bp.route('/shifts')
def add_shift():
    form = ShiftForm()
    return render_template("/schedule/shifts.html",form = form)


@bp.route('/add_availability', methods=['GET', 'POST'])
def add_availability():
    form = AvailabilityForm()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if form.validate_on_submit():
        print("Form submitted successfully!")
        # Process form data
        availability = {}
        for i, day in enumerate(days_of_week):
            if form.days[i].available.data:
                if form.days[i].all_day.data:
                    availability[day.lower()] = {'start': '00:00', 'end': '23:59'}
                else:
                    availability[day.lower()] = {
                        'start': form.days[i].start_time.data.strftime('%H:%M'),
                        'end': form.days[i].end_time.data.strftime('%H:%M')
                    }
        print("User Availability:", availability)
    else:
        print("Form failed", form.errors)
    return render_template('/schedule/availability.html', form=form, days_of_week=days_of_week)


    
