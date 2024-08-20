from fake_useragent import UserAgent


class RandomUserAgentMiddleware:
    def __init__(self):
        self.user_agent = UserAgent()

    def process_request(self, request, spider):
        request.headers["User-Agent"] = self.user_agent.random

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
