from unittest import IsolatedAsyncioTestCase

from sqli.dao.student import Student
from tests.support import Database


class StudentDAOTests(IsolatedAsyncioTestCase):
    async def test_student_list_pagination(self):
        db = Database()
        try:
            db.raw.execute('INSERT INTO students VALUES (?, ?)', (3, 'Charlie'))
            students = await Student.get_many(db)
            first = await Student.get_many(db, limit=2, offset=0)
            second = await Student.get_many(db, limit=2, offset=2)
            beyond_end = await Student.get_many(db, limit=2, offset=3)
            self.assertEqual(len(first), 2)
            self.assertEqual(len(second), 1)
            self.assertEqual(first + second, students)
            self.assertEqual(beyond_end, [])
        finally:
            db.raw.close()

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
