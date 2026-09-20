from unittest import IsolatedAsyncioTestCase

from sqli.dao.student import Student
from tests.support import Database


class StudentDAOTests(IsolatedAsyncioTestCase):
    async def test_student_search_by_partial_name(self):
        db = Database()
        try:
            before = await Student.get_many(db)
            # Both terms have no matching student; the quote must remain literal data.
            expected = await Student.get_many(db, name='Nobody')
            actual = await Student.get_many(db, name="Nobody'")
            self.assertEqual(actual, expected)
            self.assertEqual(await Student.get_many(db), before)
        finally:
            db.raw.close()
