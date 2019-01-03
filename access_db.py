import MySQLdb

queries = { "primary": "SELECT * FROM chemical WHERE chemical_id = ANY ( SELECT primary_antibody_id FROM primary_antibody )",
            "staining": "SELECT * FROM chemical WHERE chemical_id = ANY ( SELECT staining_id FROM staining )"
            }

# --------------------- DB FUNCTIONS ---------------------- #

# Queries list of primary antibodies or staining chemicals
def query(option,cursor):
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

# Returns the name of a chemical given the chemical_id
def get_chemical_name(id,cursor):

    sql = "SELECT * FROM chemical WHERE chemical_id = %s" % (id)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            return row[1]

    except:
        print "Error: unable to fetch data"

#Returns the name of a researcher given the researcher_id
def get_researcher_name(id,cursor):

    sql = "SELECT * FROM researcher WHERE researcher_id = %s" % (id)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            return row[1]

    except:
        print "Error: unable to fetch data"

# Returns the dilution of the primary antibody given the primary_ab_id
def get_pa_dilution(pa_id,cursor):
    sql = "SELECT dilution FROM primary_antibody WHERE primary_antibody_id = %s" % pa_id

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: Primary antibody %s not found" % pa_id

    return result[0]

# Returns the animal where a primary antibody was grown
def get_pa_animal(pa_id,cursor):
    sql = "SELECT animal FROM primary_antibody WHERE primary_antibody_id = %s" % pa_id

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: Primary antibody %s not found" % pa_id

    return result[0]

# Returns the secondary antibody that binds to the given primary antiobody and staining chemical
def get_sec_antibody(pa_id,s_id,cursor):
    sql = "SELECT secondary_antibody_id FROM binding WHERE primary_antibody_id = %s and staining_id = %s " % (pa_id,s_id)

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: No secondary antibody found for pa_id: %s and staining_id: %s " % (pa_id,s_id)

    return result[0]

# Prints list of reseachers
def show_researchers(cursor):
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

# Returns the remaining amount of a chemical considering reservations.
def check_availability(chemical_id,cursor):

    sql = "SELECT * FROM inventory_chemical WHERE chemical_id = %s" % (chemical_id)
    amount = 0
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            amount = row[2]

    except:
        print "Error: unable to fetch data"


    res_amount = check_reserved(chemical_id,cursor)

    for reserve in res_amount:
        amount -= reserve

    return amount

# Returns amount of chemical that has been reserved by any researcher.
def check_reserved(chemical_id,cursor):

    sql = "SELECT * FROM experiment_chemical WHERE chemical_id = %s" % (chemical_id)
    amount = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            amount.append(row[2])

    except:
        print "Error: unable to fetch data"

    return amount

# Creates a new experiment in the database
def create_experiment(researcher_id,n_slices,db,cursor):
    sql = "INSERT INTO experiment (researcher_id,tissue_slices) VALUES (%s,%s)" % (researcher_id,n_slices)

    try:
        cursor.execute(sql)
        db.commit()
        return cursor.lastrowid
    except:
        db.rollback()
        return -1

#Returns the id of the last experiment made
def get_last_experiment_id(cursor):
    sql = "SELECT experiment_id FROM experiment ORDER BY experiment_id DESC LIMIT 1"

    try:
        cursor.execute(sql)
        experiment_id = cursor.fetchone()
        return experiment_id
    except:
        print("Error obtaining last experiment id")
        return -1
# Inserts in the database the reserved chemicals for the given experiment
def reserve_chemicals(experiment_id,chemicals,db,cursor):

    for chemical in chemicals:

        sql = "INSERT INTO experiment_chemical(experiment_id,chemical_id,amount)VALUES (%s,%s,%s)" % (experiment_id,chemical[0],chemical[1])

        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()

        except:
           # Rollback in case there is any error
           db.rollback()
