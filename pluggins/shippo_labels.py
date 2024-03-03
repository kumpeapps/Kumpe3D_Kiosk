import shippo
from core.params import Params as params

shippo.config.api_key = params.SHIPPO.api_key

address_from = {
    "name": "Kumpe3D by KumpeApps LLC",
    "street1": "8180 Elm Ln",
    "city": "Rogers",
    "state": "AR",
    "zip": "72756",
    "country": "US"
}

address_to = {
    "name": "Cindy Kumpe",
    "street1": "1654 Grant 58",
    "city": "Sheridan",
    "state": "AR",
    "zip": "72150",
    "country": "US"
}

parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "6.7",
    "mass_unit": "oz"
}

shipment = shippo.Shipment.create(
    address_from = address_from,
    address_to = address_to,
    parcels = [parcel]
)

print(shipment)