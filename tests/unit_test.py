import os
import sys
import unittest

sys.path.append(".")
from SQLiteAsJSON import ManageDB  # noqa


class DB_Test(unittest.TestCase):
    def setUp(self):
        self.db = ManageDB('my_test_database.db', './tests/db_config_sample.json')

    def test_create_table(self):
        create_table_status = self.db.create_table()
        self.assertEqual(create_table_status, {"Success": "Table Created"})

    def test_insert_record(self):
        insert_table_status = self.db.insert_data(
            'my_table', {"email": 'a@b.com', 'password': 'password', "personID": '1'})
        self.assertEqual(insert_table_status, {"Success": "Data Inserted"})

    def test_search_record(self):
        search_results = self.db.search_data('my_table', {"search": "email='a@b.com'"})
        self.assertTrue(type(search_results) == list)

    def test_update_record(self):
        search_results = self.db.search_data('my_table')
        recordID = search_results[0]['id']
        self.db.update_data('my_table', recordID, {"update": "email='abc@example.com'"})
        search_results = self.db.search_data('my_table', {"search": f"id='{recordID}'"})
        self.assertEqual(search_results[0]['email'], 'abc@example.com')
        os.remove("my_test_database.db")


if __name__ == '__main__':
    unittest.main()
