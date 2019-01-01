"""
Author: Mariska Temming, S1106242
Summary: The database_helper initialize the database (three tables) and execute queries (insert data into the database)
"""

import sqlite3


def get_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file """
    try:
        conn = sqlite3.connect(db_file)  # param db_file: database file
        print("Opened database successfully!")
        return conn
    except ConnectionError as e:
        print(e)

    return None


def initialize_database():
    conn = get_connection("SFT.db")
    c = conn.cursor()

    # create four tables into database
    c.execute("CREATE TABLE IF NOT EXISTS malware_detection(name TEXT, hash REAL, path TEXT, time_detection TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS system_specifications(serial_number TEXT, disk_name TEXT, file_fomat TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS case_information(case_name TEXT, start_number REAL, investigator_name TEXT, "
              "comment TEXT, time TEXT)")

    conn.commit()  # commit the queries
    conn.close()  # close the connection with database
    print("Database initialized.")

    return None


def insert_data_malware_detection(malware):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    c.execute("INSERT INTO malware_detection(name, hash, path, time_detection) "
              "VALUES(?, ?, ?, ?)", (malware.get_name(), malware.get_hash(), malware.get_path(), malware.get_time()))
    conn.commit()
    conn.close()


def insert_data_system_specifications(system_specs):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    c.execute("INSERT INTO system_specifications(serial_number, disk_name, file_fomat) "
              "VALUES(?, ?, ?)", (system_specs.get_serial_number(), system_specs.get_disk_name(),
                                  system_specs.get_file_fomat()))

    conn.commit()
    conn.close()


def insert_data_case_information(case_data):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    c.execute("INSERT INTO case_information(case_name, start_number, investigator_name, comment, time) "
              "VALUES(?, ?, ?, ?, ?)", (case_data.get_case_name(), case_data.get_start_number(),
                                        case_data.get_investigator_name(), case_data.get_comment(),
                                        case_data.get_time()))
    conn.commit()
    conn.close()


def select_database():
    conn = get_connection("SFT.db")
    c = conn.cursor()

    print("\n" + "Table: case_information")
    for row in c.execute("SELECT * FROM case_information"):
        print(row)

    print("\n" + "Table: system_specifications")
    for row in c.execute("SELECT * FROM system_specifications"):
        print(row)

    print("\n" + "Table: malware_detection")
    for row in c.execute("SELECT * FROM malware_detection"):
        print(row)

    conn.commit()
    conn.close()


def main():
    initialize_database()


if __name__ == '__main__':
    main()
