import psycopg2
from psycopg2 import Error

# def psqlImportCSV(file_name):
#     for %%f in (*.csv):
#         with open('%%f.csv', 'r') as f:
#     # Notice that we don't need the `csv` module.
#         next(f) # Skip the header row.
#         cur.copy_from(f, 'users', sep=',')
    
try:
    # Connect to an existing database
    connection = psycopg2.connect(user="meng",password="IAOeng19910804",database="simglucose")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Add a new column into the database "results"
    # add_column = """alter table results add column Patient_ID, serial;"""
    # cursor.execute(add_column)
    # print_table = """\dt"""
    # cursor-execute(print_table)
    # cursor.fetchall()
    copyTable = """ copy results(time,bg,cgm,cho,insulin,lbgi,hbgi,risk) 
    from STDIN delimiter ',' NULL as '' csv header; """
    # Copy .CSV table into Postgresql
    f = open(r'/home/meng/Bloodglucose/results/2020-12-20_22-32-29/adolescent#002.csv', 'r')
    # next(f)
    cursor.copy_expert(copyTable, f)
    f.close()
    
    connection.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")