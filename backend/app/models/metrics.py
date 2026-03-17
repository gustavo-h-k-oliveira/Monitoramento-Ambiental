from enum import Enum

class Metric(str, Enum):
    
    temperature = "temperature"
    humidity = "humidity"
    lux = "lux"
    