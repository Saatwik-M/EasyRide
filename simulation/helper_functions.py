from datetime import datetime
import random
from flask import Flask
from easy_ride.models import User, LoginLog, RideLog, Transaction, Review, Repair, BikeInfo, TopUp
from easy_ride import db
from easy_ride.helpers import format_categories, Cnv2Obj

# Repair function for operator
def repair_bike(form, current_user):
    repair = Repair.query.filter_by(bike_number=form.bike_number, repair_status='NO').first() # Get the repair for the bike
    repair.repaired(current_user.id, form.level_of_repair, form.comment) #Update the record with details from operator
    bike = BikeInfo.query.filter_by(bike_number=repair.bike_number).first() #Get bike info and update the status from REPAIR to YES (Available)
    bike.status = 'YES'
    db.session.add_all([repair, bike]) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'OPERATOR: repaired',',', form.__dict__, )

# Move function for operator
def move_bike(form):
    bike = BikeInfo.query.filter_by(bike_number=form.bike_number).first() #Get the bike from database
    bike.place_back(form.new_location) # Update the bike location
    db.session.add(bike) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'OPERATOR: moved',',', form.__dict__)

# Register function for user
def register_user(form):
    user = User(first_name=form.first_name, last_name=form.last_name, phone_number=form.phone_number, email=form.email,
                password=form.password, city=form.city, user_type='NORMAL') # Add new user details
    db.session.add(user) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'Registered',',', form.__dict__)

# Login function for user
def login_user(form, current_user):
    login_log = LoginLog(current_user.id, current_user.user_type.name) # Add new loging log
    db.session.add(login_log) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'Logged In',',', {'user_id': current_user.id, 'user_type': current_user.user_type.name})

# Rent function for user
def rent_bike(form, current_user):
    current_rides = RideLog.query.filter_by(user_id = current_user.id, current = 'YES').first() # Get the on-going rides of the user
    payment = Transaction.query.filter_by(user_id = current_user.id, paid = 'NO').first() # Get the pending payments of the user
    if payment is None and current_rides is None: # If there are no pending payments or on-going rides only then allow them to rent
        bike = BikeInfo.query.filter_by(last_location=form.location, status='YES').first() # Get a random available bike from the selected location
        if bike is not None:
            ride = RideLog(user_id = current_user.id, bike_number = bike.bike_number, start_location = form.location, current = "YES") # Create a ride for the user
            bike.status = 'NO' # Update the bike status from YES (available) to 'NO' (not available)
            user = User.query.filter_by(id=current_user.id).first() # Get the user details and update the session variable to control the options available to him on the dashboard
            user.session_var = 'RENTED'
            db.session.add_all([user, ride, bike]) #Add and commit the changes to the database
            db.session.commit()
            print(datetime.today(),',', 'Rented',',', form.__dict__)

# Return function for user
def return_bike(form, current_user):
    current_ride = RideLog.query.filter_by(user_id = current_user.id, current = 'YES').first() # Get the on-going ride of the user
    if current_ride is not None: # IF there is an on-going ride only hten allow him to return
        bike = BikeInfo.query.filter_by(bike_number=current_ride.bike_number).first() # Get the bike info of the ride
        minutes = current_ride.get_minutes(datetime.utcnow())
        amount = 1 + int(minutes*0.2) # Calculate the amount to charge the user
        user = User.query.filter_by(id=current_user.id).first() # Get the user details

        # Only allow to proceed to payment if a user choose to pay with card or has enough balance in the wallet to pay
        if (form.payment_type == "CARD") or (form.payment_type == "WALLET" and user.wallet_balance > amount):
            # Update the ride_log, add a transaction and update the bike status
            current_ride.end_ride(form.location)
            bike.place_back(form.location)
            transaction = Transaction(user_id = current_ride.user_id,
                                       payment_type = form.payment_type,
                                       amount = amount,
                                       ride_id = current_ride.ride_id,
                                       paid = 'NO')
            user.session_var = 'PAYMENT'
            # Add rating if given
            if form.rating:
                review = Review(current_ride.user_id, current_ride.ride_id, form.rating, form.review)
                db.session.add(review)
            db.session.add_all([current_ride, bike, transaction, user]) #Add and commit the changes to the database
            db.session.commit()
            print(datetime.today(),',', 'Returned',',', form.__dict__)
            return True
        else: return False

# Payment function for user
def payment(form, current_user):
    transaction = Transaction.query.filter_by(user_id=current_user.id, paid='NO').first() # Check any pending payments to be made for the user
    if transaction is not None:
        user = User.query.filter_by(id=current_user.id).first()
        # Deduct from wallet or card as specified by the user at end of the ride
        if transaction.payment_type.name == 'WALLET':
            user.deduct_wallat_balance(transaction.amount)
            user.session_var = ''
            transaction.update_payment()
        else:
            ride = RideLog.query.filter_by(ride_id = transaction.ride_id).first()
            today = datetime.today()
            transaction.update_payment(form.card)
            user.session_var = ''
        db.session.add_all([user, transaction]) #Add and commit the changes to the database
        db.session.commit()
        print(datetime.today(),',', 'Payed',',', form.__dict__)

# Balance function for user
def add_balance(form, current_user):
    # Get user details and add to the current balance
    user = User.query.filter_by(id=current_user.id).first()
    user.add_wallet_balance(form.amount)
    # Add a topup transaction
    topup = TopUp(user_id = user.id,
                   credit_card_number = form.card,
                   amount = form.amount)
    db.session.add_all([user,topup]) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'Added Balance',',', form.__dict__)

# Report function for user
def report_bike(form, current_user):
    repair = Repair(user_id = current_user.id, bike_number = form.bike_number, description = form.description, urgency=form.urgency) # Create a repair record
    bike = BikeInfo.query.filter_by(bike_number=form.bike_number).first()
    # Only make the bike unavailble to others if the urgency is medium or high not low
    if not form.urgency == 'LOW':
        bike.status = 'REPAIR'
    db.session.add_all([repair,bike]) #Add and commit the changes to the database
    db.session.commit()
    print(datetime.today(),',', 'Reported',',', form.__dict__)
