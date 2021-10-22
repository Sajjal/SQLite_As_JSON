import sqlite3
import uuid
import time
import json
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s")

db_logger = logging.getLogger("ManageDB")


class ManageDB:
    """Takes in database name, and database config file path"""

    def __init__(self, db_name, db_config_file_path):
        self.conn = sqlite3.connect(db_name)
        self.db_config_file_path = db_config_file_path
        self.db_config = self.__verify_db_config()

    def __verify_db_config(self):
        """Verifies if the database config file exists and if it is a valid JSON file"""

        try:
            db_config_file = open(self.db_config_file_path, 'r')
            db_config = db_config_file.read()
            try:
                db_config_file.close()
                return json.loads(db_config)
            except Exception as e:
                db_logger.error({"Error": "DB Config file is not a valid JSON file!"})
                return None
        except Exception as e:
            db_logger.error({"Error": e})
            return None

    @staticmethod
    def __json_to_query(table_config):
        """Converts JSON object to SQL Query
        Parameters:
            table_config (dict):The SQL table info that should be created

        Returns:
            query (str): SQL query as string

        Example (table_config):
            {
                "table_name": "my_table",
                "fields": [
                    { "name": "id", "type": "char", "length": "50", "null": 1 },
                    { "name": "timestamp", "type": "char", "length": "20", "null": 0 },
                    { "name": "email", "type": "char", "length": "50", "null": 0 },
                    { "name": "password", "type": "char", "length": "50", "null": 0 }
                ],
                "config": {
                    "primary_key": "id"
                } 
            }
        """

        query = f"CREATE table {table_config['table_name']} ("
        for index, field in enumerate(table_config["fields"]):
            null = '' if field['null'] == 0 else 'NOT NULL'
            if index != len(table_config["fields"])-1:
                query = query + field['name']+' '+field['type']+f"({field['length']}) {null}, "
            else:
                primary_key = table_config['config']['primary_key']
                if not "foreign_key" in table_config['config']:
                    query = query + field['name']+' '+field['type'] + \
                        f"({field['length']}) {null}, PRIMARY KEY ({primary_key}) )"
                elif table_config['config']['foreign_key'] != {}:
                    foreign_key = table_config['config']['foreign_key']['field']
                    reference_table = table_config['config']['foreign_key']['reference_table']
                    reference_field = table_config['config']['foreign_key']['reference_table_field']
                    query = query + field['name']+' '+field['type'] + \
                        f"({field['length']}) {null}, PRIMARY KEY ({primary_key}),  FOREIGN KEY ({foreign_key}) REFERENCES {reference_table}({reference_field}))"
        return query

    @staticmethod
    def __obj_to_tuple(obj):
        """ Parse JSON object and format it for insert_data method

        Parameters:
            obj (dict): The JSON object that should be formatted

        Returns:
            dict: JSON object with keys and values formatted for insert_data method """

        keys = ''
        values = ''
        for key, value in obj.items():
            keys = f'{keys},{key}' if keys != '' else key
            values = f'{values}, :{key}' if values != '' else f':{key}'

        return {"keys": keys, "values": values}

    def create_table(self):
        """Creates table in database as defined in database config file"""

        if self.db_config == None:
            return
        try:
            # cursor object
            cursor = self.conn.cursor()
            for table in self.db_config:
                # drop query
                cursor.execute(f"DROP TABLE IF EXISTS {table['table_name']}")
                # create table
                cursor.execute(self.__json_to_query(table))

        except Exception as E:
            db_logger.error('Table Create Error : ', E)
        else:
            # commit query
            self.conn.commit()
            return({"Success": "Table Created"})

    def insert_data(self, table_name, params):
        """Takes in table name and JSON object of data to be inserted and inserts the given data in the table
        Parameters:
            table_name (str):The name of table where the data should be inserted
            params (dict): JSON object of data to be inserted

        Returns:
            Success message(dict): If the insertion was successful else none 

        Example:
             insert_data ('my_table', {"email": 'a@b.com', 'password': 'password'})
        """
        # get column names
        columns = self.__obj_to_tuple(params)
        # Create UUID
        params["id"] = uuid.uuid4().hex
        params["timestamp"] = round(time.time() * 1000)  # Current unix time in milliseconds

        # insert query
        try:
            query = (
                f'INSERT INTO {table_name} (id,timestamp,{columns["keys"]}) VALUES (:id, :timestamp, {columns["values"]})')
            self.conn.execute(query, params)
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        else:
            self.conn.commit()
            return({"Success": "Data Inserted"})

    def search_data(self, table_name, params={}):
        """Takes in table name and optional JSON object of data for conditional search and returns search result
        Parameters:
            table_name (str):The name of table where the data should be searched
            params (dict): (optional) JSON object to search conditionally

        Returns:
            results (dict): Search results as a JSON object

        Example (params):
             search_data('my_table', {"search": "id='55bd5301b331439fae2ba8572942ded5'"})
        """
        results = []
        try:
            # search query
            query = f"SELECT * from {table_name} WHERE {params['search']}" if 'search' in params else f"SELECT * from {table_name}"
            cursor = self.conn.execute(query)
            rows = cursor.fetchall()
            for element in rows:
                desc = list(zip(*cursor.description))[0]  # To get column names
                rowdict = dict(zip(desc, element))
                results.append(rowdict)

        except Exception as E:
            db_logger.error('Data Search Error : ', E)
        else:
            return results
            #print(json.dumps(results, indent=4))

    def update_data(self, table_name, id, params):
        """Takes in table name, id and JSON object of data to be updated and updates the record
        Parameters:
            table_name (str):The name of table where the record should be updated
            id (str): row id where the record should be updated
            params (dict): JSON object of data to update

        Returns:
            Success message(dict): If the update was successful else none 

        Example (params):
            update_data('my_table', '6fef5f821b354c71ad97067150ec5059', {"update": "email=abc@example.com, password=hello_world"})
        """

        try:
            # update query
            self.conn.execute(f"UPDATE {table_name} set {params['update']} where ID='{id}'")
        except Exception as E:
            db_logger.error('Data Update Error : ', E)
        else:
            self.conn.commit()
            return({"Success": "Data Updated"})

    def delete_data(self, table_name, id):
        """Takes in table name, id of record to delete and deletes the record
        Parameters:
            table_name (str):The name of table where the record should be deleted
            id (str): row id of record which should be deleted

        Returns:
            Success message(dict): If the delete operation was successful else none 

        Example (params):
            delete_data('my_table', '6fef5f821b354c71ad97067150ec5059')
        """
        try:
            # update query
            self.conn.execute(f"DELETE from {table_name} where ID='{id}'")
        except Exception as E:
            db_logger.error('Data Delete Error : ', E)
        else:
            self.conn.commit()
            return({"Success": "Data Deleted"})