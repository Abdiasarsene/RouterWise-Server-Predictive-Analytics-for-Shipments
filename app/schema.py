from pydantic import BaseModel, Field
from enum import Enum

# ===== DEFINITION DES COLONNES CATEGORIELLES ======
# Urgence de Livraison
class DeliveryUrgency(str, Enum):
    express = "Express"
    standard = "Standard"
    critical = "Critical"

# Urgence
class UrgencyLevel(str, Enum):
    low = "Low"
    high = "High"
    medium = "Medium"

# States
class State(str, Enum):
    newyork = "New York"
    northcarolina = "North Carolina"
    illinoia = "Illinoia"
    florida = "Florida"
    michigan = "Michigan"
    califonia = "California"
    ohio = "Ohio"
    georgia = "Georgia"
    pen = "Pennsylvania"
    texas = "Texas"


# Conditions saisoniières
class Weather(str, Enum):
    clear = "Clear"
    storm = "Storm"
    snow = "Snow"
    rain = "Rain"
    fog = "Fog"

# Jour de semaine
class DayWeek(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednes = "Wednesday"
    thurs = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"

# Moyen de transport
class TransportationMethod(str, Enum):
    truck = "Truck"
    airplane = "Airplane"
    train = "Train"

# 
class CarrierType(str, Enum):
    external = "External"
    internal = "Internal"
    express = "Express"
    specialized = "Specialized"

# Type de client
class ClientType(str, Enum):
    gallery = "Gallery"
    private = "Private_Collector"
    auction = "Auction_Mouse"
    museum = "Museum"

# ===== SCHEMA D'ENTREE ======

class LogistikData(BaseModel):
    transportation_cost: float = Field(..., ge=300, lt=35000, alias="Transportation_Cost")
    distance_km: float = Field(..., ge=1380, lt=4450, alias="Distance_Km")
    state: State = Field(..., alias="State")
    delivery_urgency: DeliveryUrgency = Field(..., alias="Delivery_Urgency")
    urgency_level: UrgencyLevel = Field(..., alias="Urgency_Level")
    client_type:ClientType  = Field(..., alias="Client_Type")
    carrier_type: CarrierType = Field(..., alias="Carrier_Type")
    transportation_method: TransportationMethod = Field(..., alias="Transportation_Method")
    day_of_week: DayWeek = Field(..., alias="Day_of_Week")
    weather_condition: Weather = Field(..., alias="Weather_Condition")

    class Config:
        validate_by_name = True
        from_attributes = True


# {
#   "Transportation_Cost": 1500,
#   "Distance_Km": 2100,
#   "State": "California",
#   "Delivery_Urgency": "Critical",
#   "Urgency_Level": "High",
#   "Client_Type": "Gallery",
#   "Carrier_Type": "Specialized",
#   "Transportation_Method": "Airplane",
#   "Day_of_Week": "Friday",
#   "Weather_Condition": "Clear"
# }