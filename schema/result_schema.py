# Functions to help define JSON for result objects

# define JSON for a specific qualifying result object
def qual_result_individual_serial(qualResultObj) -> dict:
    return {
        "id": str(qualResultObj["_id"]),
        "DriverNumber": qualResultObj["DriverNumber"],
        "Abbreviation": qualResultObj["Abbreviation"],
        "TeamName": qualResultObj["TeamName"],
        "FirstName": qualResultObj["FirstName"],
        "LastName": qualResultObj["LastName"], 
        "FullName": qualResultObj["FullName"],
        "CountryCode": qualResultObj["CountryCode"],
        "Position": qualResultObj["Position"],
        "Q1": qualResultObj["Q1"],
        "Q2": qualResultObj["Q2"],
        "Q3": qualResultObj["Q3"]
    }

# defines JSON for more than one qualResult object
def qual_result_list_serial(qualResultObjs) -> list:
    return [qual_result_individual_serial(qualResultObj) for qualResultObj in qualResultObjs]

# define JSON for a specific race result object
def race_result_individual_serial(raceResultObj) -> dict:
    return {
        "id": str(raceResultObj["_id"]),
        "DriverNumber": raceResultObj["DriverNumber"],
        "Abbreviation": raceResultObj["Abbreviation"],
        "TeamName": raceResultObj["TeamName"],
        "FirstName": raceResultObj["FirstName"],
        "LastName": raceResultObj["LastName"], 
        "FullName": raceResultObj["FullName"],
        "CountryCode": raceResultObj["CountryCode"],
        "Position": raceResultObj["Position"],
        "ClassifiedPosition": raceResultObj["ClassifiedPosition"],
        "GridPosition": raceResultObj["GridPosition"],
        "Time": raceResultObj["Time"],
        "Status": raceResultObj["Status"],
        "Points": raceResultObj["Points"]
    }

# defines JSON for more than one raceResult object
def race_result_list_serial(raceResultObjs) -> list:
    return [race_result_individual_serial(raceResultObj) for raceResultObj in raceResultObjs]