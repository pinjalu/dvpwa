import re

from tests.support import ViewCase


class CourseViewTests(ViewCase):
    async def test_course_list_visible_to_all(self):
        anonymous = await self.client.get('/courses/')
        await self.login()
        student = await self.client.get('/courses/')
        self.db.raw.execute('UPDATE users SET is_admin = TRUE WHERE id = 1')
        admin = await self.client.get('/courses/')
        for audience, response in [('anonymous', anonymous), ('student', student), ('admin', admin)]:
            with self.subTest(audience=audience):
                self.assertEqual(response.status, 200)
                page = await response.text()
                self.assertIn('Math', page)
                self.assertIn('Physics', page)

    async def test_course_page_renders_reviews(self):
        self.db.raw.execute('INSERT INTO course_reviews (course_id, review_text) VALUES (?, ?)',
                            (1, 'A useful course'))
        await self.login()
        response = await self.client.get('/courses/1')
        self.assertIn('A useful course', await response.text())

    async def test_review_post_accepted(self):
        await self.login()
        response = await self.client.get('/courses/1/review')
        page = await response.text()
        # Obtain the real context processor's token even on branches without a hidden field.
        review_form = re.search(r'<form class="col s12".*?</form>', page, re.S).group()
        token = re.search(r'name="_csrf_token" value="([^"]+)"', review_form)
        if token:
            token = token.group(1)
        else:
            token = await self.review_token()
        response = await self.client.post('/courses/1/review',
            data={'review_text': 'A useful course', '_csrf_token': token}, allow_redirects=False)
        self.assertEqual(response.status, 302)

    async def test_course_detail_requires_enrolment(self):
        await self.login()
        enrolled = await self.client.get('/courses/1')
        self.assertEqual(enrolled.status, 200)
        not_enrolled = await self.client.get('/courses/2')
        self.assertEqual(not_enrolled.status, 403)
