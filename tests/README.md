# Fixture tests

Create a Python 3.12 virtual environment and install `tests/requirements.txt`.
Run from the repository root with `python -m unittest discover -s tests -v`.

No upstream tests existed. These use unittest, an actual SQLite query engine
behind the async DAO interface, a memory Redis transport, and actual aiohttp
routes, session middleware, and Jinja rendering. No external servers are needed.

The release branches are independent. The student assertion belongs to 2026.10,
password verification to 2026.11, and course-detail enrolment to 2026.12. These
assertions intentionally fail on branches that do not contain their fixes.
On a combined checkout of the three releases, twelve tests pass and the login
throttle assertion fails normally. There are no expected-failure markers.

The five additional cases cover student pagination, clearing authentication on
logout, a session storage instance configured with a 60-second lifetime, rejection
of a correct password stored with the old unsalted MD5 digest, and course-list
visibility for anonymous visitors, students, and administrators. All five pass
on the combined release snapshot. Legacy-digest rejection also passes on
2026.11, and deliberately fails on branches that retain the MD5 implementation.
