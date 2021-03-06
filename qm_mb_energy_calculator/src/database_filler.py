import sqlite3
import pickle
import itertools
import psi4
import configparser
import sys
from database import Database
import calculator

def fill_database(settings, database_name, directory):
    """
    Walks through a database and calculates all missing energies
    
    settings is the .ini file to use to fill this database

    database_name is file the database is stored in

    directory is unued. # should probably be removed.

    """
    # add .db to the database name if it doesn't already end in .db
    if database_name[-3:] != ".db":
        print("Database name \"{}\" does not end in database suffix \".db\". Automatically adding \".db\" to end of database name.".format(database_name))
        database_name += ".db"

    database = Database(database_name) 

    print("Filling database {}".format(database_name))

    # parse settings.ini file
    config = configparser.SafeConfigParser(allow_no_value=False)

    # See if a config file already exists; if not, generate one
    config.read(settings)

    while True:
        # get a calculation to perform from the database
        calculation = database.get_missing_energy()

        # if there are no calculations left to perform, exit the loop
        if calculation is None:
            break
        
        # calculate the missing energy
        calculation.energy = calculator.calculate_energy(calculation.molecule, calculation.fragments, calculation.method + "/" + calculation.basis, True if calculation.cp == "True" else False, config)

        # update the energy in the database
        database.set_energy(calculation)

    # commit changes to database
    database.save()
    database.close()

    print("Filling of database {} successful".format(database_name))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Incorrect number of arguments");
        print("Usage: python database_filler.py <settings_file> <database_name> <directory>")
    fill_database(sys.argv[1], sys.argv[2], sys.argv[3])
