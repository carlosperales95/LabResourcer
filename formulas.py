from access_db import *

# -------------- CHEMICAL FORMULA FUNCTIONS --------------- #

# Returns the chemicals needed for a certain step and number of slices
def get_chem_step(step, n_slices):
    steps={"degrease":2,"antigen":3,"wash":5,"coverslip":8}
    quant = (n_slices//8)+1
    quant = 60 * quant
    return steps[step], quant

# Returns chemicals needed for preparing first blocking solution for given number of slices
def get_chem_block1(n_slices):

    chems = []
    quant = (n_slices//8)+1
    quant1 = 5.14 * quant
    quant2 = 54.86 * quant

    chems.append((4, quant1))
    chems.append((5, quant2))

    return chems

# Returns chemicals needed for preparing second blocking solution for given number of slices
def get_chem_block2(n_slices):

    total = (n_slices * 0.2) + 0.1
    nds = total * 0.03
    triton = total * 0.025
    tbs = total-nds-triton
    chems = [(7,nds),(6,triton),(5,tbs)]

    return chems

# Returns amount of primary antibody for the given number of slices
def get_chem_prim_antibody(n_slices, pa_id,cursor):

    chems = get_chem_block2(n_slices)
    total = (n_slices * 0.2) + 0.1

    pa_dilution = get_pa_dilution(pa_id,cursor)

    final_dilution = pa_dilution/2 #Get pa_diution from query
    pa_amount = total / final_dilution
    chems.append((pa_id,pa_amount))

    return chems

# Returns amount of secondary antibody for the given primary antibody and the number of slices
def get_chem_sec_antibody(n_slices, pa_id, s_id,cursor):

    secondary_id = get_sec_antibody(pa_id,s_id,cursor)

    return secondary_id, (n_slices * 0.1)

#Returns amount of staining chemical for the given amount of slices
def get_chem_staining(n_slices, s_id):
    return s_id, (0.2 * n_slices)
