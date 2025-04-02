
from datetime import datetime, timedelta
from flask_login import login_required, login_user, current_user
from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)
from .forms import ShiftForm, DayAvailabilityForm, AvailabilityForm
from .models import Shift, User
from . import db
import random





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
    # Clear existing test users (optional)
    User.query.filter(User.email.like("testuser%@example.com")).delete()
    db.session.commit()

    # Initialize
    user_hours = {}
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Create 9 test users with random availability
    for i in range(1, 10):
        availability = random_generated_forms()
        user = User(
            name=f"Test User {i}",
            email=f"testuser{i}@example.com",
            password="placeholder_password",
            availability=availability,
            role="employee"
        )
        db.session.add(user)
    db.session.commit()  # Commit all users at once

    # Initialize user_hours with all user IDs
    users = User.query.all()
    user_hours = {user.id: 0 for user in users}

    # Assign shifts
    for day in week:
        # Get users available on this day (with non-None availability)
        available_users = [
            user for user in users 
            if user.availability and day.lower() in user.availability
        ]
        
        open_day = [
            [user.id, user.availability[day.lower()]] 
            for user in available_users
        ]
        print(f"{day} --- {open_day}")

        # Assign shifts
        while open_day:
            assigned_user_id = assign_shift(open_day, user_hours, day)
            if not assigned_user_id:
                break
            open_day = [u for u in open_day if u[0] != assigned_user_id]

    db.session.commit()
    print("Final hours:", user_hours)



        

        
def calculate_hours(start,end):
    start_h, start_m = map(int,start.split(':'))
    end_h, end_m = map(int, end.split(':'))
    return (end_h - start_h) + (end_m - start_m) / 60


def assign_shift(day_data, user_hours, day_name):
    available_users = sorted(day_data, key=lambda x: user_hours[x[0]])
    
    if not available_users:
        return None
    
    chosen_user_id, shift_data = available_users[0]
    start_str, end_str = shift_data['start'], shift_data['end']
    
    new_shift = Shift(
        employee_id=chosen_user_id,  # Now uses the actual database ID
        start_time=datetime.strptime(start_str, '%H:%M'),
        end_time=datetime.strptime(end_str, '%H:%M'),
        day=day_name
    )
    db.session.add(new_shift)
    
    shift_hours = calculate_hours(start_str, end_str)
    user_hours[chosen_user_id] += shift_hours
    
    return chosen_user_id





 

     

@bp.route('/generate_schedule', methods=['POST','GET'])
@login_required
def generate_schedule():
    create_schedule()
    flash("Schedule generated successfully!")
    return redirect(url_for('schedule.add_availability'))


def random_generated_forms():
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    availability = {}

    # Generate random total hours between 10 and 40
    availability["total_hours"] = random.randint(10, 40)

    for day in days_of_week:
        if random.choice([True, False]):  # Randomly decide if the day is available
            if random.choice([True, False]):  # Randomly decide if it's all day
                availability[day.lower()] = {'start': '00:00', 'end': '23:59'}
            else:
                start_hour = random.randint(0, 20)  # Random start hour
                start_minute = random.choice([0, 15, 30, 45])  # Random start minute
                end_hour = random.randint(start_hour + 1, 23)  # Random end hour after start hour
                end_minute = random.choice([0, 15, 30, 45])  # Random end minute

                start_time = f"{start_hour:02}:{start_minute:02}"
                end_time = f"{end_hour:02}:{end_minute:02}"

                availability[day.lower()] = {'start': start_time, 'end': end_time}

    return availability