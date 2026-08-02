import unittest

from sql_judge_utils.mysql import MysqlDatabase as Database
from sql_judge_utils.parser import get_queries


class SampleTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.submission_path = 'queries.sql'
        cls.submission_queries = get_queries(cls.submission_path)
        cls.db1 = Database('db1')
        cls.db2 = Database('db2')

        for db in [cls.db1, cls.db2]:
            db.drop()
            db.create()
            db.initf('tests/sample_initial.sql')

    def _run_test(self, index: int):
        valid_query = self.valid_queries[index]
        submission_query = self.submission_queries[index]

        col_names_1, records_1 = self.db1.run_query(valid_query)
        col_names_2, records_2 = self.db2.run_query(submission_query)
        status, message = Database.compare_query_result(
            col_names_1,
            records_1,
            col_names_2,
            records_2
        )

        print(len(records_1))
        print(records_1)
        print(len(records_2))
        print(records_2)

        self.assertTrue(status, message)
        self.assertEqual(message, '')

    def test_query_1(self):
        submission_query = self.submission_queries[0]
        self.db2.run_query(submission_query)
        query = '''
            EXPLAIN SELECT SUM(total)
            FROM orders
            WHERE created_at BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:59'
        '''
        col_names, records = self.db2.run_query(query)
        self.assertLessEqual(records[0][9], 5174)
        self.assertRegex(records[0][11], r'Using index([^\s]|$)')
