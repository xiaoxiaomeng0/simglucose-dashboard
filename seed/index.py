import psycopg2
from psycopg2 import Error

import glob
import pandas as pd
from pathlib import Path, PurePosixPath


# def psqlImportCSV(file_name):
#     for %%f in (*.csv):
#         with open('%%f.csv', 'r') as f:
#     # Notice that we don't need the `csv` module.
#         next(f) # Skip the header row.
#         cur.copy_from(f, 'users', sep=',')

try:
    # Connect to an existing database
    connection = psycopg2.connect(
        user="postgres", password="iaoeng", database="simglucose")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Add a new column into the database "results"
    # add_column = """alter table results add column Patient_ID, serial;"""
    # cursor.execute(add_column)
    # print_table = """\dt"""
    # cursor-execute(print_table)
    # cursor.fetchall()
    # copyTable = """ copy results(time,bg,cgm,cho,insulin,lbgi,hbgi,risk,patient_id)
    # from STDIN delimiter ',' NULL as '' csv header; """
    # Copy .CSV table into Postgresql

    # directory = os.path.join("/home/meng/Bloodglucose","results")

    for file in glob.glob('../results/2021-07-08_23-23-27/adolescent#001.csv'):
        df = pd.read_csv(file)
        print(df)
        # if "Patient_ID" in df.columns:
        #     df = df.drop(columns=['Patient_ID'])
        # df["patient_id"] = PurePosixPath(file).stem
        # df.to_csv(file, index=False)
        # f=open(file)
        # cursor.copy_expert(copyTable, f)
        f.close()

    connection.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
