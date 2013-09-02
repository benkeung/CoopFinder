import sys
import os

project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(project_root)

import sqlite3
import config

class DataHandler(object):

    table_schemas_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "table_schemas.sql")

    base_sql_statement_placepro = "INSERT or %s INTO placepro VALUES(?,?,?,?,?,?,?,?,?)"

    def __init__(self):
        self.connection = sqlite3.connect(config.path_to_db)
        self.__create_tables_if_not_already_exists()

    def insert_placepro_adapter_overwrite(self, placepro):
        """ Overwrites the existing table if it exists.
        
        NOTE: The reason we need to have a separate method and not just use the insert_placepro with a flag,
        is that it added extra complexities in how it interacted with the placepro selenium scraper
        """
        self.insert_placepro(placepro, True)

    def insert_placepro_adapter_no_overwrite(self, placepro):
        """ Does NOT Overwrite the existing table if it exists.
        
        NOTE: The reason we need to have a separate method and not just use the insert_placepro with a flag,
        is that it added extra complexities in how it interacted with the placepro selenium scraper
        """
        self.insert_placepro(placepro, False)

    def insert_placepro(self, placepro, overwrite=False):
        """
        :param placepro: dictionary format of placepro information as defined in placepro.py
        """
        sql_statement_placepro = self.__create_full_placepro_sql_statement(overwrite)

        if isinstance(placepro, dict):
            placepro = self.__convert_placepro_dict_to_tuple(placepro)
        if not isinstance(placepro, tuple):
            raise ValueError("Invalid argument: placepro has to be a dict or tuple in the appropriate format")

        cursor = self.connection.cursor()
        cursor.execute(sql_statement_placepro, placepro)

        self.connection.commit()

    def insert_many_placepro(self, many_placepro, overwrite=False):
        """
        :param many_placepro: list of valid placepro dictionary or tuple
        """
        sql_statement_placepro = self.__create_full_placepro_sql_statement(overwrite)

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
            cursor.executemany(sql_statement_placepro,placepro)
            self.connection.commit()

    def set_in_calendar(self, placepro_id, in_calendar=1):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE placepro SET in_calendar=? WHERE Id=?", (in_calendar, placepro_id))
        self.connection.commit()

    def is_in_calendar(self, placepro_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT in_calendar FROM placepro WHERE id = ?", (placepro_id,))
        is_in_calendar = cursor.fetchone()[0]

        # returns 0 or 1
        return is_in_calendar

    def get_placepro_by_id(self, placepro_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM placepro WHERE id = ?", (placepro_id,))

        return cursor.fetchall()

    def get_placepro_by_keyword_flag(self, has_keyword):
        if has_keyword:
            has_keyword = 1
        else:
            has_keyword = 0

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM placepro WHERE contains_keyword = ?", (has_keyword,))

        return cursor.fetchall()

    def get_all_placepro(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from placepro")

        return cursor.fetchall()

    def close_connection(self):
        self.connection.close()

    def __convert_placepro_dict_to_tuple(self, placepro_dict):
        placepro_tuple = (
            placepro_dict["id"],
            placepro_dict["posting_title"],
            placepro_dict["company_name"],
            placepro_dict["url"],
            placepro_dict["location"],
            placepro_dict["resume_deadline"],
            placepro_dict["job_description"],
            placepro_dict["contains_keyword"],
            False,)

        return placepro_tuple

    def __create_tables_if_not_already_exists(self):
        connection = sqlite3.connect(config.path_to_db)
        cursor = connection.cursor()

        with open(self.table_schemas_file_name, "rb") as sql:
            table_schema = sql.read()
            cursor.executescript(table_schema)

        connection.commit()

    def __create_full_placepro_sql_statement(self, overwrite):
        if overwrite:
            return self.base_sql_statement_placepro % "REPLACE"
        return self.base_sql_statement_placepro % "IGNORE"
