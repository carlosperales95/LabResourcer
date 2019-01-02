from access_db import get_pa_animal

# ------------------------- UTILS ------------------------- #

# Function to delete tuples inside a list and convert to a list
def dissolve_inTuple(dest_array, orig_array):
    for item in orig_array:
        dest_array.append(item)


# Function to join in a list tuples that contain the same chemicals.
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

# Function to check if primary antibodies come from different animal and can be stained in the same process
def check_compatibility(primaries,cursor):

    animals = []
    for idx, primary in enumerate(primaries):
        animals.append(get_pa_animal(primary,cursor))

    for idx, animal in enumerate(animals):
        result = indexall(animals, animal)
        if len(result) == 1:
            continue

    return(result)

#Function to obtain the indeces of a list
def indexall(list, value):
    return [i for i, v in enumerate(list) if v == value]
