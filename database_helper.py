import sqlite3

from database.malware import Malware


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
    c.execute("CREATE TABLE IF NOT EXISTS system_specifications(disk_name TEXT, serial_number REAL, file_fomat TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS case_information(case_name TEXT, investigator_name TEXT, path TEXT, "
              "time TEXT, task TEXT)")
    # c.execute("CREATE TABLE IF NOT EXISTS virustotal(malware_name TEXT, malware_hash REAL)")
    #  mogelijk geen bestand inladen van virustotal....

    conn.commit()   # commit the queries
    conn.close()    # close the connection with database
    print("Database initialized.")

    return None


def insert_data_malware_detection(malware_data):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    for item in malware_data:
        c.execute("INSERT INTO malware_detection(name, hash, path, time_detection) "
                  "VALUES(?, ?, ?, ?)", (item.get_name(), item.get_hash(), item.get_path(), item.get_time()))
    conn.commit()
    conn.close()


def insert_data_system_specifications(system_data):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    for item in system_data:
        c.execute("INSERT INTO system_specifications(disk_name, serial_number, file_fomat) "
                  "VALUES(?, ?, ?, ?)", (item.get_disk_name(), item.get_serial_number(), item.get_file_fomat()))
    conn.commit()
    conn.close()


def insert_data_case_information(case_data):
    conn = get_connection("SFT.db")
    c = conn.cursor()

    for item in case_data:
        c.execute("INSERT INTO case_information(case_name, investigator_name, path, time, time) "
                  "VALUES(?, ?, ?, ?)", (item.get_case_name(), item.get_investigator_name(), item.get_path(),
                                         item.get_time(), item.get_task))
    conn.commit()
    conn.close()


def main():
    initialize_database()

    # test
    # m1 = Malware('hoi', '1234123', '/pad/', '2018')
    # m2 = Malware('doei', '45643', '/niiew/', '2019')
    # list = [m1, m2]

    # insert_data_malware_detection(malware_data)   # input a list in the function
    # insert_data_system_specifications(system_data)    # input a list in the function
    # insert_data_case_information(case_data)   # input a list in the function


if __name__ == '__main__':
    main()
