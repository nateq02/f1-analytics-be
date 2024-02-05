# Functions to help define JSON for event objects

# define JSON for a specific event
def event_individual_serial(event) -> dict:
    return {
        "id": str(event["_id"]),
        "RoundNumber": event["RoundNumber"],
        "Location": event["Location"],
        "OfficialEventName": event["OfficialEventName"],
        "EventDate": event["EventDate"],
        "EventName": event["EventName"],
        "EventFormat": event["EventFormat"],
        "Session1": event["Session1"],
        "Session1Date": event["Session1Date"],
        "Session1DateUtc": event["Session1DateUtc"],
        "Session2": event["Session2"],
        "Session2Date": event["Session2Date"],
        "Session2DateUtc": event["Session2DateUtc"],
        "Session3": event["Session3"],
        "Session3Date": event["Session3Date"],
        "Session3DateUtc": event["Session3DateUtc"],
        "Session4": event["Session4"],
        "Session4Date": event["Session4Date"],
        "Session4DateUtc": event["Session4DateUtc"],
        "Session5": event["Session5"],
        "Session5Date": event["Session5Date"],
        "Session5DateUtc": event["Session5DateUtc"],
        "F1ApiSupport": event["F1ApiSupport"]
    }

# defines JSON for more than one event
def event_list_serial(events) -> list:
    return [event_individual_serial(event) for event in events]