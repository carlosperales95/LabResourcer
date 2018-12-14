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


def get_chemical_name(id):

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


def get_researcher_name(id):

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


def get_pa_dilution(pa_id):
    sql = "SELECT dilution FROM primary_antibody WHERE primary_antibody_id = %s" % pa_id

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: Primary antibody %s not found" % pa_id

    return result[0]


def get_pa_animal(pa_id):
    sql = "SELECT animal FROM primary_antibody WHERE primary_antibody_id = %s" % pa_id

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: Primary antibody %s not found" % pa_id

    return result[0]


def get_sec_antibody(pa_id,s_id):
    sql = "SELECT secondary_antibody_id FROM binding WHERE primary_antibody_id = %s and staining_id = %s " % (pa_id,s_id)

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print "Error: No secondary antibody found for pa_id: %s and staining_id: %s " % (pa_id,s_id)

    return result[0]


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


def check_availability(chemical_id):

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


    res_amount = check_reserved(chemical_id)

    for reserve in res_amount:
        amount -= reserve
        print "- %.3f" %(reserve)

    print "Available quant: %.3f" %(amount)
    return amount


def check_reserved(chemical_id):

    sql = "SELECT * FROM experiment_chemical WHERE chemical_id = %s" % (chemical_id)
    amount = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            amount.append(row[2])
            print(amount)

    except:
        print "Error: unable to fetch data"

    return amount



def get_chem_step(step, n_slices):
    steps={"degrease":2,"antigen":3,"wash":5,"coverslip":8}
    quant = (n_slices//8)+1
    quant = 60 * quant
    return steps[step], quant


def get_chem_block1(n_slices):

    chems = []
    quant = (n_slices//8)+1
    quant1 = 5.14 * quant
    quant2 = 54.86 * quant

    chems.append((4, quant1))
    chems.append((5, quant2))

    return chems


def get_chem_block2(n_slices):

    total = (n_slices * 0.2) + 0.1
    nds = total * 0.03
    triton = total * 0.025
    tbs = total-nds-triton
    chems = [(7,nds),(6,triton),(5,tbs)]

    return chems


def get_chem_prim_antibody(n_slices, pa_id):

    chems = get_chem_block2(n_slices)
    total = (n_slices * 0.2) + 0.1

    pa_dilution = get_pa_dilution(pa_id)

    final_dilution = pa_dilution/2 #Get pa_diution from query
    pa_amount = total / final_dilution
    chems.append((pa_id,pa_amount))

    return chems


def get_chem_sec_antibody(n_slices, pa_id, s_id):

    secondary_id = get_sec_antibody(pa_id,s_id)

    return secondary_id, (n_slices * 0.1)


def get_chem_staining(n_slices, s_id):
    return s_id, (0.2 * n_slices)


def dissolve_inTuple(dest_array, orig_array):
    for item in orig_array:
        dest_array.append(item)


def join_equals(list):
    chemicals = {}

    for item in list:
        if item[0] in chemicals:
            chemicals[item[0]]+=item[1]
        else:
            chemicals[item[0]]=item[1]

    chem_list = []

    #Converting back to list
    for key,value in chemicals.iteritems():
        chem_list.append((key,value))

    return chem_list


def get_chem_simple():

    chemicals = []
    chemicals.append(get_chem_step("degrease")) #degrease
    chemicals.append(get_chem_step("antigen"))#antigen
    chemicals.append(get_chem_step("wash"))#wash
    chems = get_chem_block1()#block1
    dissolve_inTuple(chemicals, chems)
    chemicals.append(get_chem_step("wash"))#wash
    chems = get_chem_block2()#block2
    dissolve_inTuple(chemicals, chems)
    chems = get_chem_prim_antibody()#pa
    dissolve_inTuple(chemicals, chems)
    chemicals.append(get_chem_step("wash"))#wash
    chemicals.append(get_chem_sec_antibody())#sa
    chemicals.append(get_chem_step("wash"))#wash
    chemicals.append(get_chem_staining())#staining
    chemicals.append(get_chem_step("wash"))#wash
    chemicals.append(get_chem_step("coverslip"))#coverslip

    return chemicals


def check_compatibility(primaries):

    animals = []
    for idx, primary in enumerate(primaries):
        animals.append(get_pa_animal(primary))

    for idx, animal in enumerate(animals):
        result = indexall(animals, animal)
        if len(result) == 1:
            continue

    return(result)


def indexall(list, value):
    return [i for i, v in enumerate(list) if v == value]


def header_block(chemicals, n_slices):

    #chemicals.append(get_chem_step("degrease", n_slices)) #degrease
    chemicals.append(get_chem_step("antigen", n_slices))#antigen
    chemicals.append(get_chem_step("wash", n_slices))#wash

    chems = get_chem_block1(n_slices)#block1
    dissolve_inTuple(chemicals, chems)

    chemicals.append(get_chem_step("wash", n_slices))#wash

    chems = get_chem_block2(n_slices)#block2
    dissolve_inTuple(chemicals, chems)


def step_PaSaS(chemicals, n_slices, pa_id, s_id):

    chems = get_chem_prim_antibody(n_slices, pa_id)#pa
    dissolve_inTuple(chemicals, chems)

    #single wash step located outside in calculate_variation_steps()

    chemicals.append(get_chem_sec_antibody(n_slices, pa_id, s_id))#sa
    chemicals.append(get_chem_step("wash", n_slices))#wash

    chemicals.append(get_chem_staining(n_slices, s_id))#staining
    chemicals.append(get_chem_step("wash", n_slices))#wash


def repeating_block(chemicals, n_slices, pa_id , s_id):
    header_block(chemicals, n_slices)
    step_PaSaS(chemicals, n_slices, pa_id , s_id)
    chemicals.append(get_chem_step("wash", n_slices))#wash


def calculate_variation_steps(n_slices, primaries, stainings):

    chemicals = []
    equal_pas = check_compatibility(primaries)
    #print(equal_pas)
    chemicals.append(get_chem_step("degrease", n_slices)) #degrease

    if len(equal_pas) == 1:
        #print "Todos diferentes: "
        for index, primary in enumerate(primaries):
            #print "Pasada - "
            repeating_block(chemicals, n_slices, primary, stainings[index])
        #print "\n"
    else:
        #print "Algunos estan iguals: "
        remaining_p = primaries[:]
        remaining_s = stainings[:]
        header_block(chemicals, n_slices)
        for item in equal_pas:
            step_PaSaS(chemicals, n_slices, primaries[item], stainings[item])
            #print(primaries)
            #print(stainings)
            num = item
            del remaining_p[0]
            del remaining_s[0]
            #print "Pasada -"

        chemicals.append(get_chem_step("wash", n_slices))#wash
        #print "\n"

        if len(remaining_p) == 1:
            #print "Parece que eran todos: "
            repeating_block(chemicals, n_slices, remaining_p.pop(0), remaining_s.pop(0))
            #print "Lonely pasada"
            #print "\n"

    chemicals.append(get_chem_step("coverslip", n_slices))#coverslip
    return chemicals


def input_PaSaloop(times):

    primaries = []
    stainings = []
    for i in range(0, times):

        print("     EXPERIMENT PREPARATION - INPUT PHASE: PRIMARY ANTIBODY SELECTION %i \n" %(i))
        print("______________________________________________________________________\n")
        print("List of Primary Antibodies:")
        query("primary")
        print("\n")
        primaries.append (int(raw_input("Please select the primary antibody %i ID that you will use in your experiment: " %(i))))
        print("\n")

        print("     EXPERIMENT PREPARATION - INPUT PHASE: STAINING SELECTION %i \n" %(i))
        print("______________________________________________________________________\n")
        print("List of Staining Methods:")
        query("staining")
        print("\n")

        stainings.append(int(raw_input("Please select the staining  %i ID you want to perform: " %(i))))
        print("\n")

    return primaries, stainings

def input_reservation():
    print("\n\n     CHEMICAL RESERVATION - INPUT PHASE \n")
    print("______________________________________________________________________\n")
    #for availability give options
    print("1.- Reserve available chemicals and request all unavailables")
    print("2.- Reserve availables and manage requests")
    print("3.- Reserve available chemicals only")
    print("4.- Cancel")

    choice = int(raw_input("\nPlease enter the desired option: "))

    if(choice < 1 or choice > 4):
        print("%i is not an option.",choice)
        choice = input_reservation()
    else:
        return choice

def input_phase():

    print("-------------------------------------------------------------------- \n")
    print("         Welcome to LabResourcer - by Miguel and Carlos \n")
    print("-------------------------------------------------------------------- \n")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: RESEARCHER SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Researchers:")
    show_researchers()
    print("\n")
    researcher_id = int(raw_input("Please enter your researcher ID: "))
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: AMOUNT OF TISSUE \n")
    print("______________________________________________________________________\n")
    print("\n")
    n_slices = int(raw_input("Please enter the amount of slices to be used in this experiment: "))
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: STAINING METHOD \n")
    print("______________________________________________________________________\n")
    print("List of Methods:")
    print("\n")
    print("1.-Single Staining")
    print("\n")
    print("2.-Double Staining")
    print("\n")
    print("3.-Triple Staining")
    times = int(raw_input("Please enter the method to be followed: "))
    print("\n")

    primaries, stainings = input_PaSaloop(times)

    print("     EXPERIMENT PREPARATION - INPUT PHASE: PROTOCOL SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Protocols:")
    #query("protocol")
    print("\n")

    return researcher_id,n_slices,primaries,stainings


def calculation_phase(n_slices, primaries, stainings):

    chemicals = calculate_variation_steps(n_slices, primaries, stainings)
    print(chemicals)
    print "\n"
    chemicals = join_equals(chemicals)

    return chemicals

def create_experiment(researcher_id,n_slices):
    sql = "INSERT INTO experiment (researcher_id,tissue_slices) VALUES (%s,%s)" % (researcher_id,n_slices)

    try:
        cursor.execute(sql)
        db.commit()
        return cursor.lastrowid
    except:
        db.rollback()
        return -1


def reserve_chemicals(experiment_id,chemicals):

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

def split_chemicals_availability(chemicals):
    available = []
    unavailable = []

    for chemical in chemicals:
        if chemical[2]>=0:
            available.append((chemical[0],chemical[1])) #Append chemcal_id and amount Needed
        else:
            unavailable.append((chemical[0],chemical[2]*(-1))) #Append chemical_id and necessary amount to request

    return available, unavailable

def output_phase(chemicals, researcher_id, n_slices, primaries, stainings):


    researcher_name = get_researcher_name(researcher_id)

    print("     EXPERIMENT PREPARATION - OUTPUT PHASE\n")
    print("________________________\n")
    print "Researcher: %s - ID(%i) \n" %(researcher_name, researcher_id)
    print("Experiment ID: \n")
    print "Number of slices: %i \n" %(n_slices)

    for index, primary in enumerate(primaries):
        primary_name = get_chemical_name(primaries[index])
        staining_name = get_chemical_name(stainings[index])
        print "Primary Antibody %i: %s - ID(%i) \n" %((index+1), primary_name, primaries[index])
        print "Staining Method %i: %s - ID(%i) \n" %((index+1), staining_name, stainings[index])

    print("\n")
    print("List of Chemicals Needed:")
    print("=========================")
    #list with availability

#    for id, amount in chemicals:
#        name = get_chemical_name(id)
#        print "(%i)%s - %.3f ml" % (id, name, amount)


    chemicals = reservation_phase(chemicals)

    #print(chemicals)

    print("\n")

    for id, amount, am_available  in chemicals:
        name = get_chemical_name(id)
        if am_available >= 0:
            #print "(%i)%s - %.3f ml - AVAILABLE" % (id, name, amount)
            print "(%i)%s - AVAILABLE " %(id,name)
        else:
            print "(%i)%s - UNAVAILABLE " %(id,name)

            #print "(%i)%s - %.3f ml - UNAVAILABLE" % (id, name, amount)

    #############
    #RESERVATION
    # 1.- Reserve available chemicals and request all unavailables
    # 2.- Reserve availables and manage requests
    # 3.- Reserve available chemicals only
    # 4.- Cancel
    ##############
    available, unavailable = split_chemicals_availability(chemicals)

    print("\n AVAILABLE")
    for id, amount in available:
        name = get_chemical_name(id)
        print "(%i) %s %.3f" % (id,name,amount)

    print("\n UNAVAILABLE")
    for id, amount in unavailable:
        name = get_chemical_name(id)
        print "(%i) %s %.3f" % (id,name,amount)

    choice = input_reservation()

    if choice == 4:
        print "Experiment cancelled"
    else:
        experiment_id = create_experiment(researcher_id,n_slices)
        reserve_chemicals(experiment_id,available)
        if choice == 1:
            print("Chemicals reserved. All unavaiables should be requested")
            #Request unavailable
        elif choice == 2:
            print("Chemicals reserved. Manage unavailable chemicals")
            #Manage request unavailables


def reservation_phase(chemicals):

    final_chemicals = []

    for id, quantity in chemicals:
        #print(id)
        #print(quantity)
        amount = check_availability(id)
        #print(amount)
        final_chemicals.append((id, quantity, (amount-quantity)))
        #print "Am-q: %.3f" % (amount-quantity)

    #print(final_chemicals)

    return final_chemicals

def execution():

    researcher_id, n_slices, primaries, stainings = input_phase()

    print("Calculating values with the experiment input...")
    print("\n")


    chemicals = calculation_phase(n_slices, primaries, stainings)

    output_phase(chemicals, researcher_id, n_slices, primaries, stainings)



# Open database connection
db = MySQLdb.connect("localhost",credentials.username,credentials.password,"lab_resourcer" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

execution()

#print(chemicals)

#def inventory_checkup():
    #query to check the amounts available for chemicals[] in inventory and add status to dest_array




db.close()



'''
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
'''
