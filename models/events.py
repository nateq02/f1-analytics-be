# Defines a BaseModel that represents the structure of an event object
    # used for data validation

from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    RoundNumber: int
    Country: str
    Location: str
    OfficialEventName: str
    EventDate: datetime
    EventName: str
    EventFormat: str
    Session1: str
    Session1Date: str
    Session1DateUtc: datetime
    Session2: str
    Session2Date: str
    Session2DateUtc: datetime    
    Session3: str
    Session3Date: str
    Session3DateUtc: datetime
    Session4: str
    Session4Date: str
    Session4DateUtc: datetime    
    Session5: str
    Session5Date: str
    Session5DateUtc: datetime
