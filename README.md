## App details
### Hosting details
 **Hosted platform** : ~~Heroku~~  
 **Main Domain Name** : ~~www.easyride.live~~  
 **Heroku app deployed domain** : ~~easyridelab02.herokuapp.com~~  

### Login information for testing
**User**
>Register as a new user  

**Operator**
>**email** : o1@easyride.live  
**password** : 12345666

>Can also register a new operator from manager dashboard

**Manager**
>**email** : manager@easyride.live  
**password** : 12345666

### Database information
**username** = ~~admin~~  
**password** = ~~lab02g2c~~  
**endpoint** = ~~group-project-psd.clsvl0h7k6t3.eu-west-2.rds.amazonaws.com:3306~~  
**database** = ~~easy_ride~~  

>Hosted at AWS RDS

### For local deployment

1. Open the command line terminal at the main project folder  
2. Install the required libraries mentioned in the requirements.txt file  
```bash
pip install -r requirements.txt  
```
3. If migrations folder is not available, then initialize the flask db
```bash
flask db init  
```
4. If any new changes were made to the models.py file, then migrate the changes  
```bash
pip install -r requirements.txt  
```
3. If migrations folder is not available, then initialize the flask db
```bash
flask db init  
```
4. If any new changes were made to the models.py file, then migrate the changes  
```bash
flask db migrate -m "changes made"
flask db upgrade
```
5. Start the app by running the app.py file  
```bash
python app.py
```
6. Visit 127.0.0.1:5000 where the app is deployed  


## Some cool project stats

| Type | Lines | Chars | Files | Percent | Comments |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Python | 1793 | 112814 | 23 | 52.3 | 506 |
| HTML | 2142 | 87823 | 32 | 40.1 | 244 |
| CSS | 160 | 3249 | 2 | 1.5 | 11 |
| JavaScript | 411 | 11544 | 2 | 5.4 | 56 |
| **Total** | **4506** | **215430** | **59** | **100** | **817** |


## Directory Structure:

```
EasyRide
|   app.py (File which launches the flask application)
|   Procfile (File required for hosting in heroku)
|   project_stats.py (Gets the project statistics)
|   requirements.txt (The required python libraries for the application)
|   
+---easy_ride (Contains the main project files)
|   |   helpers.py (Contains some reusable helper functions used in other files)
|   |   models.py (Defines the database tables, columns and their values)
|   |   __init__.py  (Initiates the flask application and register the blueprints)
|   |   
|   +---core  (contains the files related to basic functionality such as home page, about etc.)
|   |   |   forms.py (contains the forms related to basic functionality)
|   |   |   views.py (contains the routes related to basic functionality)
|   |   |   
|   |           
|   +---employees (contains the files related to employees functionality such as operator, manager views etc.)
|   |   |   forms.py (contains the forms related to employees functionality)
|   |   |   views.py (contains the routes related to employees functionality)
|   |   |   
|   |           
|   +---error_pages (contains the files related to error functionality such as 403, 404)
|   |   |   handlers.py (contains the routes related to error pages)
|   |   |   
|   |           
|   +---rides (contains the files related to ride functionality such as rent, return etc.)
|   |   |   forms.py (contains the forms related to ride functionality)
|   |   |   views.py (contains the routes related to ride functionality)
|   |   |   
|   |           
|   +---static
|   |   +---css (contains styling files)
|   |   |       style.css
|   |   |       
|   |   +---js (contains javascript files for charts configs and maps)
|   |   |       chart_config.js
|   |   |       glasgow_location_map.js
|   |   |       
|   |   \---profile_pics (stores the profile images)
|   |           default_profile.jpg
|   |           
|   +---templates (contains all the HTML files required to render by the routes in all views.py files)
|   |   |   aboutus.html (Static About us page)
|   |   |   account.html (User Profile page)
|   |   |   account_layout.html (sideNavbar layout for the account tab. Will be reused in all account related pages)
|   |   |   addbalance.html (Add wallet balance page)
|   |   |   base.html (Main Navbar layout. Used in all pages)
|   |   |   booking.html (Booked ride details including bike number, pin etc.)
|   |   |   check_bikes.html (Check bikes details and their status for operators and managers)
|   |   |   check_rides.html (Check ride details for operators and managers)
|   |   |   employee_layout.html (Navbar layout for the employee views. Will be reused in all employee related pages)
|   |   |   howitworks.html (Static how the application works page)
|   |   |   index.html (Static home page)
|   |   |   locations.html (Static available locations page)
|   |   |   login.html (User login page)
|   |   |   manager_home.html (Manage dashboard)
|   |   |   move_bike.html (Move bike form page for operators)
|   |   |   operators.html (All operator details for manager)
|   |   |   operator_home.html (Operator dashboard)
|   |   |   payment.html (Ride payment page)
|   |   |   placeback.html (Bike return page)
|   |   |   pricing.html (Static pricing page)
|   |   |   register.html (User registration page)
|   |   |   rent.html (Bike renting page)
|   |   |   repair_bike.html (Defective bike repair page for operators)
|   |   |   reportbike.html (Defective bike report page for users)
|   |   |   trackbike.html (Bike details and tracking page for operators and managers)
|   |   |   userreviews.html (Past user reviews list page)
|   |   |   userrides.html (Past user ride history page)
|   |   |   users.html (All user details for manager)
|   |   |   user_info.html (Bike info and history page for operators and managers)
|   |   |   wallet.html (Wallet balance page)
|   |   |   
|   |   \---error_pages (Error HTML render pages)
|   |           403.html
|   |           404.html
|   |           
|   +---users (contains the files related to user account functionality such as register, login, history etc.)
|   |   |   forms.py (contains the forms related to users functionality)
|   |   |   picture_handler.py (contains the function for updating the profile picture)
|   |   |   views.py (contains the routes related to users functionality)
|   |   |   
|   |           
|           
+---migrations (Autogenerated Migrations folder by flask-migrate to keep track of database modifications)
|   |           
|
+---simulation (Contains the testing simulation files)
|   |   config.py (Contains some variables for simulation)
|   |   helper_functions.py (Defines functions for simulating various actions)
|   |   simulation.py  (A simulation file which acts on behalf of users and operators to test the application)     
```
