# Defines a BaseModel that represents the structure of standings objects
    # used for data validation

from pydantic import BaseModel
from datetime import datetime

class DriverStandingObj(BaseModel):
    position: int
    positionText: str
    points: int
    wins: int
    driverId: str
    driverNumber: int
    driverCode: str
    driverUrl: str
    givenName: str
    familyName: str
    dateOfBirth: datetime
    driverNationality: str
    constructorIds: list
    constructorUrls: list
    constructorNames: list
    constructorNationalities: list
    year: int

class ConstructorStandingObj(BaseModel):
    position: int
    positionText: str
    points: int
    wins: int
    constructorId: str
    constructorUrl: str
    constructorName: str
    constructorNationality: str
    year: int
