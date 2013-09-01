import sys
import os

project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(project_root)

import sqlite3
import config

class DataHandler(object):

    table_schemas_file_name = "table_schemas.sql"

    sql_statement_placepro = "INSERT INTO placepro VALUES(?,?,?,?,?,?,?,?)",

    def __init__(self):
        self.connection = sqlite3.connect(config.path_to_db)
        self.__create_tables_if_not_already_exists()

    def insert_place_pro(self, placepro):
        """
        :param placepro: dictionary format of placepro information as defined in placepro.py
        """
    
        if isinstance(placepro, dict):
            placepro = self.__convert_placepro_dict_to_tuple(placepro)
        if not isinstance(placepro, tuple):
            raise ValueError("Invalid argument: placepro has to be a dict or tuple in the appropriate format")

        cursor = self.connection.cursor()

        cursor.execute(self.sql_statement_placepro, placepro)


    def insert_many_place_pro(self, many_placepro):
        """
        :param many_placepro: list of valid placepro dictionary or tuple
        """
        # Convert all placepros to tuple if not already
        placepro = []
        for pp in many_placepro:
            if isinstance(placepro, dict):
                pp = self.__convert_placepro_dict_to_tuple(placepro)
            if not isinstance(placepro, tuple):
                print "WARNING: Not in proper format...\nData: %r" % pp
            placepro.append(pp)

        if placepro.count() != 0:
            cursor = self.connection.cursor()
            cursor.executemany(self.sql_statement_placepro,placepro)

    def close_connection():
        self.connection.close()

    def __convert_placepro_dict_to_tuple(self, placepro_dict):
        placepro_tuple = (
            placepro["id"],
            placepro["posting_title"],
            placepro["company_name"],
            placepro["url"],
            placepro["location"],
            placepro["resume_deadline"],
            placepro["job_description"],
            placepro["contains_keyword"])

        return placepro_tuple

    def __create_tables_if_not_already_exists(self):
        connection = sqlite3.connect(config.path_to_db)
        cursor = connection.cursor()

        with open(self.table_schemas_file_name, "rb") as sql:
            table_schema = sql.read()
            print table_schema
            cursor.executescript(table_schema)

        connection.commit()

# For testing
if __name__ == "__main__":
    datahandler = DataHandler()
    datahandler.create_tables_if_not_already_exists()