# Functions to help define JSON for standing objects

# define JSON for a specific driver standing object
def driver_standing_individual_serial(driverStandingObj) -> dict:
    return {
        "id": str(driverStandingObj["_id"]),
        "position": driverStandingObj["position"],
        "positionText": driverStandingObj["positionText"],
        "points": driverStandingObj["points"],
        "wins": driverStandingObj["wins"],
        "driverId": driverStandingObj["driverId"],
        "driverNumber": driverStandingObj["driverNumber"],
        "driverCode": driverStandingObj["driverCode"],
        "driverUrl": driverStandingObj["driverUrl"],
        "givenName": driverStandingObj["givenName"],
        "familyName": driverStandingObj["familyName"],
        "dateOfBirth": driverStandingObj["dateOfBirth"],
        "driverNationality": driverStandingObj["driverNationality"],
        "constructorIds": driverStandingObj["constructorIds"],
        "constructorUrls": driverStandingObj["constructorUrls"],
        "constructorNames": driverStandingObj["constructorNames"],
        "constructorNationalities": driverStandingObj["constructorNationalities"],
        "year": driverStandingObj["year"]
    }

# defines JSON for more than one driverStanding object
def driver_standing_event_list_serial(driverStandingObjs) -> list:
    return [driver_standing_individual_serial(driverStandingObj) for driverStandingObj in driverStandingObjs]

# define JSON for a specific driver standing object
def constructor_standing_individual_serial(constructorStandingObj) -> dict:
    return {
        "id": str(constructorStandingObj["_id"]),
        "position": constructorStandingObj["position"],
        "positionText": constructorStandingObj["positionText"],
        "points": constructorStandingObj["points"],
        "wins": constructorStandingObj["wins"],
        "constructorId": constructorStandingObj["constructorId"],
        "constructorUrl": constructorStandingObj["constructorUrl"],
        "constructorName": constructorStandingObj["constructorName"],
        "constructorNationality": constructorStandingObj["constructorNationality"],
        "year": constructorStandingObj["year"]
    }

# defines JSON for more than one driverStanding object
def constructor_standing_event_list_serial(constructorStandingObjs) -> list:
    return [constructor_standing_individual_serial(constructorStandingObj) for constructorStandingObj in constructorStandingObjs]
