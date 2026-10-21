from .mock_collector import mock_calendar
class EconomicCalendarProvider:
    def fetch(self): return mock_calendar()
