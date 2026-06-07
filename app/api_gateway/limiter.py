class RateLimiter:
    def __init__(self, key, max_attempts, window_seconds):
        self.key, self.max_attempts, self.window_seconds = key, max_attempts, window_seconds

    def hit(self, ip):
        pass  # backed by redis in prod

LOGIN_LIMIT = RateLimiter(key="login:{ip}", max_attempts=5, window_seconds=300)

def check_login_rate(ip):
    LOGIN_LIMIT.hit(ip)
