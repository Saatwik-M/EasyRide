"""
A simulation bot to act on behalf of both user (for actions
registering, renting, paying etc) and an operator (for moving and
repairing)

This is used to run in AWS EC2 instance where it runs continuosly
in the background  in order to test the solution
"""

from datetime import datetime
import random
from flask import Flask
from easy_ride.models import User, LoginLog, RideLog, Transaction, Review, Repair, BikeInfo, TopUp
from easy_ride import db
from easy_ride.helpers import format_categories, Cnv2Obj
from config import *
from helper_functions import *

# Keep the script running
while True:
    time = datetime.today()
    if time.minute in random.choices(range(0,60), k=3):  # A way to control the probability
        # Register user
        try:
            if random.uniform(0, chance) < 0.005: # A way to control the probability
            # Get random details of name, email and register a new user
                first_name = random.choice(first_name_choices)
                last_name = random.choice(last_name_choices)
                email_suffix = random.choice(email_suffix_choices)
                form = Cnv2Obj(dict(first_name=first_name, last_name=last_name, phone_number=random.randint(1000000000, 9999999999),
                                    email=first_name+last_name+email_suffix+str(random.randint(10000, 99999))+'@dummy.test', password='12345666', city='GLASGOW'))
                register_user(form)
        except Exception as e: ''

        # Rent
        try:
            if random.uniform(0, chance) < 10: # A way to control the probability
            # Choose a random user then both perform a login and also rent a bike from him from a random location
                user = random.choice(User.query.filter_by( user_type='NORMAL').all())
                if user.first_name in first_name_choices:
                    form = Cnv2Obj(dict(location = random.choice(locations)))
                    login_user(form, user)
                    rent_bike(form, user)
        except Exception as e: ''

        # Return
        try:
            if random.uniform(0, chance) < 1: # A way to control the probability
            # Choose a random on going ride then finish ride with random payment method, a random rating and comment
                user = random.choice(RideLog.query.filter_by( current='YES').all()).user
                if user.first_name in first_name_choices:
                    rating = random.choice([1,1,1,2,2,3,3,3,3,3,4,4,4,5,5,5,5,5,5,5])
                    payment_type = random.choice(['CARD','CARD','WALLET','WALLET','WALLET'])
                    form = Cnv2Obj(dict(location = random.choice(locations), payment_type=payment_type,
                                        rating = rating, review = random.choice(comments[rating])))

                    if return_bike(form, user): # If return is succesful i.e. choosen card or have enough balance to pay via the wallet
                        if payment_type == 'WALLET': # If choosen to pay with wallet then deduct balance from the users wallet and update the transaction
                            payment(form, user)
                    else:
                        form.payment_type = 'CARD' # If choose to pay with wallet but doesnt have enough balance to pay then update the payment method to card and return the bike
                        return_bike(form, user)
        except Exception as e: ''

        # Payment
        try:
            if random.uniform(0, chance) < 2: # A way to control the probability
            # Choose a random pending payment and finish the payment with random card details
                user = random.choice(Transaction.query.filter_by(paid = 'NO').all()).user
                if user.first_name in first_name_choices:
                    form = Cnv2Obj(dict(name = 's', card=int(str(random.randint(9999999, 100000000)) + str(random.randint(9999999, 100000000))),
                                    month = '05', year = '2023', cvv = '123'))
                    payment(form, user)
        except Exception as e: ''

        # TopUp
        try:
            if random.uniform(0, chance) < 1: # A way to control the probability
            # Choose a random user and topup the wallet balance if it is below 10
                user = random.choice(User.query.filter_by( user_type='NORMAL').all())
                if user.first_name in first_name_choices:
                    if user.wallet_balance < 10:
                        form = Cnv2Obj(dict(amount = random.randint(5, 50), name = 's', card=int(str(random.randint(9999999, 100000000)) + str(random.randint(9999999, 100000000))),
                                            month = '05', year = '2023', cvv = '123'))
                        add_balance(form, user)
        except Exception as e: ''

        # Report
        try:
            if random.uniform(0, chance) < 1: # A way to control the probability
            # Choose a random user and have him report a random bike with random urgency and descriptions
                user = random.choice(User.query.filter_by( user_type='NORMAL').all())
                if user.first_name in first_name_choices:
                    bike = random.choice(BikeInfo.query.filter_by(status='YES').all())
                    urgency =  random.choice(['LOW','MEDIUM','HIGH'])
                    form = Cnv2Obj(dict(bike_number = bike.bike_number, urgency=urgency, description=random.choice(descriptions[urgency])))
                    report_bike(form, user)
        except Exception as e: ''

        # Repair bike
        try:
            if random.uniform(0, chance) < 1: # A way to control the probability
            # Choose a random report and have a random operator repair it with random level of repair and random comments
                user = random.choice(User.query.filter_by(user_type='OPERATOR').all())
                repair = random.choice(Repair.query.filter_by(repair_status='NO').all())
                if BikeInfo.query.filter_by(bike_number=repair.bike_number).first().status.name in ['YES', 'REPAIR']:
                    level_of_repair = random.choice(repair_levels[repair.urgency.name])
                    form = Cnv2Obj(dict(bike_number = repair.bike_number, level_of_repair = level_of_repair,
                                        comment = random.choice(repair_comments[level_of_repair])))
                    repair_bike(form, user)
        except Exception as e: ''
        # Move bike
        try:
            if random.uniform(0, chance) < 10: # A way to control the probability
            # Check if there are less than 4 bikes in any location, then move bike to each of those location from a location with most bikes
                avl_bikes_raw = dict(BikeInfo.query.filter_by(status = 'YES').with_entities(BikeInfo.last_location.name, db.func.count(BikeInfo.last_location).label('count')).group_by(BikeInfo.last_location).all())
                avl_bikes = dict(format_categories(avl_bikes_raw, ['HILLHEAD', 'PARTICK', 'GOVAN', 'FINNIESTON', 'LAURIESTON']))
                low_number_loc = []
                high_number_loc = max(avl_bikes, key=avl_bikes.get)
                for loc in avl_bikes:
                    if avl_bikes[loc] < 4:
                        low_number_loc.append(loc)
                if low_number_loc:
                    for low_loc in low_number_loc:
                        bike = BikeInfo.query.filter_by(last_location = high_number_loc, status='YES').first()
                        if bike is not None:
                            form = Cnv2Obj(dict(bike_number = bike.bike_number, new_location = low_loc))
                            move_bike(form)
        except Exception as e: ''

    # Every one hour finsh all the on-going rides and all pending repairs
    if time.minute == 30:
        # Return all bikes
        try:
            returns = RideLog.query.filter_by( current='YES').all() # Get all on going rides
            for to_return in returns:
                # Choose a random on going ride then finish ride with random payment method, a random rating and comment
                user = to_return.user
                if user.first_name in first_name_choices:
                    rating = random.choice([1,1,1,2,2,3,3,3,3,3,4,4,4,5,5,5,5,5,5,5])
                    payment_type = random.choice(['CARD','CARD','WALLET','WALLET','WALLET'])
                    form = Cnv2Obj(dict(location = random.choice(locations), payment_type=payment_type,
                                          rating = rating, review = random.choice(comments[rating])))
                    if return_bike(form, user):
                        if payment_type == 'WALLET':
                            payment(form, user)
                    else:
                        form.payment_type = 'CARD'
                        return_bike(form, user)
        except Exception as e: ''
        # Pay all
        try:
            payments = Transaction.query.filter_by(paid = 'NO').all() # Get all pending payments
            for to_pay in payments:
                # Choose a random pending payment and finish the payment with random card details
                user = to_pay.user
                if user.first_name in first_name_choices:
                    form = Cnv2Obj(dict(name = 's', card=int(str(random.randint(9999999, 100000000)) + str(random.randint(9999999, 100000000))),
                                    month = '05', year = '2023', cvv = '123'))
                    payment(form, user)
        except Exception as e: ''
