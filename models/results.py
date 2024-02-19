# Defines a BaseModel that represents the structure of standings objects
    # used for data validation

from pydantic import BaseModel

class QualifyingResultsObj(BaseModel):
    DriverNumber: str
    Abbreviation: str
    TeamName: str
    FirstName: str
    LastName: str
    FullName: str
    CountryCode: str
    Position: int
    Q1: int
    Q2: int
    Q3: int

class RaceResultObj(BaseModel):
    DriverNumber: str
    Abbreviation: str
    TeamName: str
    FirstName: str
    LastName: str
    FullName: str
    CountryCode: str
    Position: int
    ClassifiedPosition: str
    GridPosition: int
    Time: float
    Status: str
    Points: int