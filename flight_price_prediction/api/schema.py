from pydantic import BaseModel, Field
from typing import Literal

class FlightInput(BaseModel):
    airline: Literal[
        'Air_Asia', 'Air_India', 'GO_FIRST',
        'Indigo', 'SpiceJet', 'Vistara'
    ]
    source_city: Literal[
        'Bangalore', 'Chennai', 'Delhi',
        'Hyderabad', 'Kolkata', 'Mumbai'
    ]
    destination_city: Literal[
        'Bangalore', 'Chennai', 'Delhi',
        'Hyderabad', 'Kolkata', 'Mumbai'
    ]
    departure_time: Literal[
        'Early_Morning', 'Morning', 'Afternoon',
        'Evening', 'Night', 'Late_Night'
    ]
    arrival_time: Literal[
        'Early_Morning', 'Morning', 'Afternoon',
        'Evening', 'Night', 'Late_Night'
    ]
    stops: Literal['zero', 'one', 'two_or_more']
    travel_class: Literal['Economy', 'Business']
    duration: float = Field(..., gt=0, description="Flight duration in hours")
    days_left: int  = Field(..., gt=0, description="Days before departure")

    class Config:
        json_schema_extra = {
            "example": {
                "airline": "Indigo",
                "source_city": "Delhi",
                "destination_city": "Mumbai",
                "departure_time": "Morning",
                "arrival_time": "Afternoon",
                "stops": "zero",
                "travel_class": "Economy",
                "duration": 2.5,
                "days_left": 30
            }
        }

class PredictionOutput(BaseModel):
    predicted_price: float
    price_range: str
    advice: str