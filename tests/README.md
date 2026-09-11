# Tests

Create a Python 3.12 virtual environment and install `tests/requirements.txt`.
Run from the repository root with `python -m unittest discover -s tests -v`.

The suite uses an in-memory SQLite query engine behind the async DAO interface,
a memory Redis transport, and live aiohttp routes, session middleware and Jinja
rendering. No external services are required.
