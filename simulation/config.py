chance = 500000 # Probabilty factor to control how often the simulation performs any given actions

# Variables with random values required for some actions
# Required for registering the new users
first_name_choices = 'Kent Cian Eamon Emrys Ansel Finnick Chester Evander Lysander Keiran Liesel Aiko Aaralyn Imogen Adora Andromeda Odette Acacia Aoife Alaska Artemis Ocean Adalia Indigo Ash Darcy Avalon Echo Billie Zephyr'.split()
last_name_choices = 'Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez Martinez Hernandez Lopez Gonzalez Wilson Anderson Thomas Taylor Moore Jackson Martin Lee Perez Thompson White Harris Sanchez Clark Ramirez Lewis Robinson'.split()
email_suffix_choices = ['', '', '', '', '', '91', '92', '93', '94', '95', '96', '97', '98', '007', 'cool', 'zzz', 'always']
# Required for renting, returning and rating the rides for the users
locations = 'HILLHEAD HILLHEAD HILLHEAD HILLHEAD PARTICK PARTICK FINNIESTON FINNIESTON FINNIESTON GOVAN LAURIESTON LAURIESTON'.split() # Same location given multiple times to control the probabilty for each location
comments = {1:['', '', '', '', '', '', '', '', 'Bad ride', 'dissapointing ride', 'should take better care of your bikes'], \
            2:['', '', '', '', '', '', '', '', 'Not very good', 'dissapointing', 'bikes not in very good condition'], \
            3:['', '', '', '', '', '', '', '', 'Ok ok', 'Not very good', 'add more locations'], \
            4:['', '', '', '', '', '', '', '', 'Good', 'good service', 'satisfiying ride', 'nice bikes provided'], \
            5:['', '', '', '', '', '', '', '', 'Great ride', 'very good', 'extremely good', 'great service provided by easy ride']} # Different comment for different ratings
#  required for reporting a bike by the users
descriptions = {'LOW':['Small scratch', 'Paint lost', 'Handle is loose'], \
               'MEDIUM':['Handle very loose', 'Frame is rattling', 'Frame bent a bit'], \
               'HIGH':['Handle broken', 'Frame bent', 'Tyre punchured']} # Different desciptions for different level of repairs for users to report
# Required for repairing for the operators
repair_levels = {'LOW':[1,2], 'MEDIUM':[2,3,4], 'HIGH':[3,4,5]}
repair_comments = {1: ['Fixed', 'Small issue'], 2: ['fixed', 'Not a big issue'], 3: ['All done', 'Fixed', 'Able to fix'], 4: ['Big issue', 'issue with handle', 'issue with frame'], 5: ['Type issue', 'issue with handle', 'issue with frame']}
