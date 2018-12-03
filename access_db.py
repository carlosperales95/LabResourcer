#!/usr/bin/python
import credentials
import MySQLdb

queries = { "primary": "SELECT * FROM chemical WHERE chemical_id = ANY ( SELECT primary_antibody_id FROM primary_antibody )",
            "staining": "SELECT * FROM chemical WHERE chemical_id = ANY ( SELECT staining_id FROM staining )"
            }

def query(option):
    sql = queries[option]
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
          chemid = row[0]
          chemname = row[1]
          # Now print fetched result
          print "%s.- %s" % (chemid, chemname)
    except:
       print "Error: unable to fetch data"

def show_researchers():
    sql = "SELECT * FROM researcher"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       researchers = cursor.fetchall()
       for researcher in researchers:
          researcher_id = researcher[0]
          researcher_name = researcher[1]
          # Now print fetched result
          print "%s.- %s" % (researcher_id,researcher_name)
    except:
       print "Error: unable to fetch researchers"

def get_inputValues():
    print("-------------------------------------------------------------------- \n")
    print("         Welcome to LabResourcer - by Miguel and Carlos \n")
    print("-------------------------------------------------------------------- \n")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: RESEARCHER SELECTION \n")
    print("______________________________________________________________________\n")
    show_researchers()
    print("List of Researchers:")
    print("\n")
    researcher_id = raw_input("Please enter your researcher ID: ")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: AMOUNT OF TISSUE \n")
    print("______________________________________________________________________\n")
    print("\n")
    slices_n = raw_input("Please enter the amount of slices to be used in this experiment: ")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: PRIMARY ANTIBODY SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Primary Antibodies:")
    query("primary")
    print("\n")
    primary_id = raw_input("Please select the primary antibody ID that you will use in your experiment: ")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: STAINING METHOD SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Staining Methods:")
    query("staining")
    print("\n")
    primary_id = raw_input("Please select the staining ID you want to perform: ")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: PROTOCOL SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Protocols:")
    #query("protocol")
    print("\n")

    print("Calculating values with the experiment input...")
    print("\n")

    print("     EXPERIMENT PREPARATION - OUTPUT PHASE\n")
    print("______________________________________________________________________\n")
    print("Researcher: \n")
    print("Experiment ID: \n")
    print("Number of slices: \n")
    print("Primary antibody: \n")
    print("Staining Method: \n")

    print("\n")
    print("List of Chemicals Needed:")
    print("=========================")
    #list with availability
    #for availability give options
    ##1. Reserve available chemicals and request all unavailables
    ##2. Reserve availables and manage requests
    ##3. Reserve available chemicals only
    ##4. Cancel
    print("\n")



# Open database connection
db = MySQLdb.connect("localhost",credentials.username,credentials.password,"lab_resourcer" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

get_inputValues()







#######READ FROM TABLE############
sql = "SELECT * FROM chemical WHERE chemical_id = ANY ( SELECT primary_antibody_id FROM primary_antibody )" \
       #WHERE INCOME > '%d'" % (1000)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      chemid = row[0]
      chemname = row[1]
      # Now print fetched result
      print "chemid=%s,chemname=%s" % \
             (chemid, chemname)
except:
   print "Error: unable to fecth data"
#####################################

#######INSERT INSTANCE TO TABLE############
# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO chemical(chemical_id,
         name)
         VALUES ('20', 'brule')"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
 #####################################


#######UPDATE TABLE############
# Prepare SQL query to UPDATE required records
sql = "UPDATE chemical SET name = 'test' WHERE chemical_id = 20"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
#####################################


#######DELETE INSTANCE FROM TABLE############
# Prepare SQL query to DELETE required records
sql = "DELETE FROM chemical WHERE name = 'test'" #% (20)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
#####################################



# disconnect from server
db.close()
