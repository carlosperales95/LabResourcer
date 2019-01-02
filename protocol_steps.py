from utils import *
from formulas import *

# Calculates chemicals for the steps Antigen retrieval, washing, first blocking solution and second blocking solution
def header_block(chemicals, n_slices):

    #chemicals.append(get_chem_step("degrease", n_slices)) #degrease
    chemicals.append(get_chem_step("antigen", n_slices))#antigen
    chemicals.append(get_chem_step("wash", n_slices))#wash

    chems = get_chem_block1(n_slices)#block1
    dissolve_inTuple(chemicals, chems)

    chemicals.append(get_chem_step("wash", n_slices))#wash

    chems = get_chem_block2(n_slices)#block2
    dissolve_inTuple(chemicals, chems)

# Calculate chemicals for Primary antibody, Secondary antibody and staining chemical
def step_PaSaS(chemicals, n_slices, pa_id, s_id,cursor):

    chems = get_chem_prim_antibody(n_slices, pa_id,cursor)#pa
    dissolve_inTuple(chemicals, chems)

    #single wash step located outside in calculate_variation_steps()

    chemicals.append(get_chem_sec_antibody(n_slices, pa_id, s_id,cursor))#sa
    chemicals.append(get_chem_step("wash", n_slices))#wash

    chemicals.append(get_chem_staining(n_slices, s_id))#staining
    chemicals.append(get_chem_step("wash", n_slices))#wash

# Calculates chemicals for header block, Primary secondary antibody and staining
def repeating_block(chemicals, n_slices, pa_id , s_id,cursor):
    header_block(chemicals, n_slices)
    step_PaSaS(chemicals, n_slices, pa_id , s_id,cursor)
    chemicals.append(get_chem_step("wash", n_slices))#wash

#Calculate neccessary chemicals depending on the origin of the primary antibody
def calculate_variation_steps(n_slices, primaries, stainings,cursor):

    chemicals = []
    equal_pas = check_compatibility(primaries,cursor)
    chemicals.append(get_chem_step("degrease", n_slices)) #degrease

    if len(equal_pas) == 1:
        for index, primary in enumerate(primaries):
            #print "Pasada - "
            repeating_block(chemicals, n_slices, primary, stainings[index],cursor)
    else:
        remaining_p = primaries[:]
        remaining_s = stainings[:]
        header_block(chemicals, n_slices)
        for item in equal_pas:
            step_PaSaS(chemicals, n_slices, primaries[item], stainings[item],cursor)
            num = item
            del remaining_p[0]
            del remaining_s[0]

        chemicals.append(get_chem_step("wash", n_slices))#wash

        if len(remaining_p) == 1:
            repeating_block(chemicals, n_slices, remaining_p.pop(0), remaining_s.pop(0),cursor)


    chemicals.append(get_chem_step("coverslip", n_slices))#coverslip
    return chemicals
