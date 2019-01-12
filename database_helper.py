"""
Author: Mariska Temming, S1106242
Summary: - The database_helper gets a connection to the database SFT.db
         - The database_helper initialize the database (SFT.db); it creates three tables: malware_detection,
           system_specifications, case_information and virusshare_hashes
         - The database_helper writes data to the database with the insert query
         - The database_helper selects the data of the database with the select query
         - The database_helper drops the tables case_information, system_specifications and malware_detection
"""

import sqlite3


# Creates a database connection to the SQLite database specified by db_file
def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("Opened database successfully!")
        return conn
    except ConnectionError as e:
        print(e)

    return None


# Initialize the database
def initialize_database():
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    # Creates three tables into the database
    c.execute("CREATE TABLE IF NOT EXISTS malware_detection(name TEXT, hash REAL, path TEXT, time_detection TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS system_specifications(serial_number TEXT, disk_name TEXT, file_fomat TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS case_information(case_name TEXT, start_number REAL, investigator_name TEXT, "
              "comment TEXT, time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS virusshare_hashes(hash TEXT)")

    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database
    print("Database initialized.")

    return None


# Inserts data into the table: malware_detection
def insert_data_malware_detection(malware):
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    c.execute("INSERT INTO malware_detection(name, hash, path, time_detection) "
              "VALUES(?, ?, ?, ?)", (malware.get_name(), malware.get_hash(), malware.get_path(), malware.get_time()))
    conn.commit()   # Commit the queries
    conn.close()  # Close the connection with the database


# Inserts data into the table: system_specifications
def insert_data_system_specifications(system_specs):
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    c.execute("INSERT INTO system_specifications(serial_number, disk_name, file_fomat) "
              "VALUES(?, ?, ?)", (system_specs.get_serial_number(), system_specs.get_disk_name(),
                                  system_specs.get_file_fomat()))
    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


# Inserts data into the table: case_information
def insert_data_case_information(case_data):
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    c.execute("INSERT INTO case_information(case_name, start_number, investigator_name, comment, time) "
              "VALUES(?, ?, ?, ?, ?)", (case_data.get_case_name(), case_data.get_start_number(),
                                        case_data.get_investigator_name(), case_data.get_comment(),
                                        case_data.get_time()))
    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


# Inserts data into the table: virusshare_hashes
def insert_data_virusshare_hashes():
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    with open('virusshare_hashes.txt') as e:
        for line in e.readlines():
            line = line.rstrip()
            print(line)
            c.execute("INSERT INTO virusshare_hashes(hash) VALUES(?)", (line,))
                  
    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


# Selects the system_hash which is in virusshare
def select_virusshare_hashes_by_system_hash(system_hash):
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    c.execute("SELECT * FROM virusshare_hashes WHERE hash=?", (system_hash,))
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


# Selects the data of the database
def select_database():
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    print("\n" + "Table: case_information")
    for row in c.execute("SELECT * FROM case_information"):
        print(row)

    print("\n" + "Table: system_specifications")
    for row in c.execute("SELECT * FROM system_specifications"):
        print(row)

    print("\n" + "Table: malware_detection")
    for row in c.execute("SELECT * FROM malware_detection"):
        print(row)

    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


# Drops the database tables case_information, system_specifications, malware_detection
def drop_database():
    conn = get_connection("SFT.db")  # Get a connection with the database
    c = conn.cursor()  # Create a cursor object to call its execute() method to perform SQL commands

    print("\n" + "Drop table: case_information")
    c.execute("DROP TABLE case_information")

    print("\n" + "Drop table: system_specifications")
    c.execute("DROP TABLE system_specifications")

    print("\n" + "Drop table: malware_detection")
    c.execute("DROP TABLE malware_detection")

    conn.commit()  # Commit the queries
    conn.close()  # Close the connection with the database


def main():
    initialize_database()
    insert_data_virusshare_hashes()


if __name__ == '__main__':
    main()



