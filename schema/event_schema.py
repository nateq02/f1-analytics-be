# Functions to help define JSON for event objects

# define JSON for a specific event
def event_individual_serial(event) -> dict:
    return {
        "id": str(event["_id"]),

    }

# defines JSON for more than one event
def event_list_serial(events) -> list:
    return [event_individual_serial(event) for event in events]