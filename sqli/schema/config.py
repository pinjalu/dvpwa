"""Single settings loader for web and queue processes."""
import os


def load_config():
    return {
        'environment': os.environ.get('DVPWA_ENV', 'production'),
        'db': {
            'user': os.environ.get('DVPWA_DB_USER', 'postgres'),
            'password': os.environ.get('DVPWA_DB_PASSWORD', 'postgres'),
            'host': os.environ.get('DVPWA_DB_HOST', 'postgres'),
            'port': int(os.environ.get('DVPWA_DB_PORT', '5432')),
            'database': os.environ.get('DVPWA_DB_NAME', 'sqli'),
        },
        'redis': {
            'host': os.environ.get('DVPWA_REDIS_HOST', 'redis'),
            'port': int(os.environ.get('DVPWA_REDIS_PORT', '6379')),
            'db': int(os.environ.get('DVPWA_REDIS_DB', '0')),
        },
        'app': {'host': '0.0.0.0', 'port': 8080, 'debug': True},
        'security': {'secret': os.environ.get('DVPWA_SECRET', 'dvpwa-evaluation-only-secret')},
        'session_cookie': {'secure': True, 'httponly': True},
    }
