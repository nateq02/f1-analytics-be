# Functions to help define JSON for event objects
from datetime import datetime

# define JSON for a specific event
def event_individual_serial(event) -> dict:
    def format_datetime(dt):
        return dt.isoformat() if isinstance(dt, datetime) else None

    return {
        "id": str(event["_id"]),
        "RoundNumber": event["RoundNumber"],
        "Location": event["Location"],
        "OfficialEventName": event["OfficialEventName"],
        "EventDate": format_datetime(event["EventDate"]),
        "EventName": event["EventName"],
        "EventFormat": event["EventFormat"],
        "Session1": event["Session1"],
        "Session1Date": format_datetime(event["Session1Date"]),
        "Session1DateUtc": format_datetime(event["Session1DateUtc"]),
        "Session2": event["Session2"],
        "Session2Date": format_datetime(event["Session2Date"]),
        "Session2DateUtc": format_datetime(event["Session2DateUtc"]),
        "Session3": event["Session3"],
        "Session3Date": format_datetime(event["Session3Date"]),
        "Session3DateUtc": format_datetime(event["Session3DateUtc"]),
        "Session4": event["Session4"],
        "Session4Date": format_datetime(event["Session4Date"]),
        "Session4DateUtc": format_datetime(event["Session4DateUtc"]),
        "Session5": event["Session5"],
        "Session5Date": format_datetime(event["Session5Date"]),
        "Session5DateUtc": format_datetime(event["Session5DateUtc"]),
        "F1ApiSupport": event["F1ApiSupport"],
        "QualifyingResult": event.get("QualifyingResult", []),
        "RaceResult": event.get("RaceResult", []),
        "SprintShootoutResult": event.get("SprintShootoutResult", []),
        "SprintResult": event.get("SprintResult", [])
    }

# defines JSON for more than one event
def event_list_serial(events) -> list:
    return [event_individual_serial(event) for event in events]