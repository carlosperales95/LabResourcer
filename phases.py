from access_db import *
from protocol_steps import *
from utils import *

# Receives input of the primary antiobody and staining chemical
def input_PaSaloop(times,cursor):

    primaries = []
    stainings = []

    for i in range(0, times):

        print("     EXPERIMENT PREPARATION - INPUT PHASE: PRIMARY ANTIBODY SELECTION %i \n" %(i+1))
        print("______________________________________________________________________\n")
        print("List of Primary Antibodies:")
        query("primary",cursor)
        print("\n")
        primaries.append (int(raw_input("Please select the primary antibody %i ID that you will use in your experiment: " %(i))))
        print("\n")

        print("     EXPERIMENT PREPARATION - INPUT PHASE: STAINING SELECTION %i \n" %(i+1))
        print("______________________________________________________________________\n")
        print("List of Staining Methods:")
        query("staining",cursor)
        print("\n")

        stainings.append(int(raw_input("Please select the staining %i ID you want to perform: " %(i+1))))
        print("\n")

    return primaries, stainings

# Outputs the chemicals that are going to be requested
def request_chemicals(chemicals,cursor):
    print "\nThe following chemicals are going to be requested:"

    for id, amount in chemicals:
        name = get_chemical_name(id,cursor)
        print "(%i) %s %.3f" % (id,name,amount)

# Receive input of the chemicals the user want to request
def manage_unavailable(unavailable,cursor):

    print "\n Unavaiable chemicals:"
    for id, amount in unavailable:
        name = get_chemical_name(id,cursor)
        print "(%i) %s %.3f" % (id,name,amount)

    choice_string = raw_input("Type ids of chemicals you want to request (comma separated): ")

    choice_ids = [int(x) for x in choice_string.split(",")]

    chemicals_to_request = []

    for id,amount in unavailable:
        if id in choice_ids:
            chemicals_to_request.append((id,amount))

    return chemicals_to_request

# Returns to arrays, one for available chemicals and another one for unavailable chemicals
def split_chemicals_availability(chemicals):
    available = []
    unavailable = []

    for chemical in chemicals:
        if chemical[2]>=0:
            available.append((chemical[0],chemical[1])) #Append chemcal_id and amount Needed
        else:
            unavailable.append((chemical[0],chemical[2]*(-1))) #Append chemical_id and necessary amount to request

    return available, unavailable

# Received input of the user to choose reservation and request of chemicals
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

# Returns the real amount of chemical left considering reservations
def availability_phase(chemicals,cursor):

    final_chemicals = []

    for id, quantity in chemicals:

        amount = check_availability(id,cursor)
        final_chemicals.append((id, quantity, (amount-quantity)))

    return final_chemicals


# --------------------------------------------------------- #



# ----------------- MAIN PROGRAM PHASES ------------------- #

# Receives input of the main program
def input_phase(cursor):

    print("-------------------------------------------------------------------- \n")
    print("         Welcome to LabResourcer - by Miguel and Carlos \n")
    print("-------------------------------------------------------------------- \n")
    print("\n")

    print("     EXPERIMENT PREPARATION - INPUT PHASE: RESEARCHER SELECTION \n")
    print("______________________________________________________________________\n")
    print("List of Researchers:")
    show_researchers(cursor)
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

    primaries, stainings = input_PaSaloop(times,cursor)

    #print("     EXPERIMENT PREPARATION - INPUT PHASE: PROTOCOL SELECTION \n")
    #print("______________________________________________________________________\n")
    #print("List of Protocols:")
    #query("protocol")
    print("\n")

    return researcher_id,n_slices,primaries,stainings

# Returns list of chemicals needed for the experiment
def calculation_phase(n_slices, primaries, stainings,cursor):

    chemicals = calculate_variation_steps(n_slices, primaries, stainings,cursor)
    chemicals = join_equals(chemicals)

    return chemicals

# Reserves and request chemicals depending on the user choice
def reservation_phase(chemicals, researcher_id, n_slices,db,cursor):

    #############
    #RESERVATION
    # 1.- Reserve available chemicals and request all unavailables
    # 2.- Reserve availables and manage requests
    # 3.- Reserve available chemicals only
    # 4.- Cancel
    ##############

    available, unavailable = split_chemicals_availability(chemicals)
    choice = input_reservation()

    if choice == 4:
        print "Experiment cancelled"

    else:
        experiment_id = create_experiment(researcher_id,n_slices,db,cursor)
        reserve_chemicals(experiment_id,available,db,cursor)
        print("\nAvailable chemicals reserved.\n")

        if choice == 1:
            request_chemicals(unavailable,cursor)
        elif choice == 2:
            chemicals_to_request = manage_unavailable(unavailable,cursor)
            request_chemicals(chemicals_to_request,cursor)

# Outputs chemicals needed for the experiment
def output_phase(chemicals, researcher_id, n_slices, primaries, stainings,cursor):


    researcher_name = get_researcher_name(researcher_id,cursor)

    print("     EXPERIMENT PREPARATION - OUTPUT PHASE\n")
    print("________________________\n")
    print "Researcher: %s - ID(%i) \n" %(researcher_name, researcher_id)
    experiment_id = int(get_last_experiment_id(cursor)[0])+1
    print "Experiment ID: %i \n" % experiment_id
    print "Number of slices: %i \n" %(n_slices)

    for index, primary in enumerate(primaries):
        primary_name = get_chemical_name(primaries[index],cursor)
        staining_name = get_chemical_name(stainings[index],cursor)
        print "Primary Antibody %i: %s - ID(%i) \n" %((index+1), primary_name, primaries[index])
        print "Staining Method %i: %s - ID(%i) \n" %((index+1), staining_name, stainings[index])

    print("\n")
    print("List of Chemicals Needed:")
    print("=========================")
    print("\n")

    chemicals = availability_phase(chemicals,cursor)

    for id, amount, am_available  in chemicals:

        name = get_chemical_name(id,cursor)

        if am_available >= 0:
            print "(%i) %s %.3f ml - AVAILABLE" % (id, name, amount)

        else:
            print "(%i) %s %.3f ml - UNAVAILABLE " %(id, name, amount)

    return chemicals
