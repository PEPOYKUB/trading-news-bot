class APICollector:
    """Extension point for licensed News/Economic Calendar APIs."""
    def __init__(self, name: str, endpoint: str, api_key: str = ""): self.name, self.endpoint, self.api_key = name, endpoint, api_key
    def fetch(self): raise NotImplementedError("Configure a licensed API adapter before enabling this source")
