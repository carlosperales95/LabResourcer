#!/usr/bin/python
import credentials
import MySQLdb
from phases import *


# Open database connection
db = MySQLdb.connect("localhost",credentials.username,credentials.password,"lab_resourcer" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

researcher_id, n_slices, primaries, stainings = input_phase(cursor)

chemicals = calculation_phase(n_slices, primaries, stainings,cursor)

chemicals = output_phase(chemicals, researcher_id, n_slices, primaries, stainings,cursor)

reservation_phase(chemicals, researcher_id, n_slices,db,cursor)

db.close()
