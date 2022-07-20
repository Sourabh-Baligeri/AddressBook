from pydantic import BaseModel, Field

class Address(BaseModel):
    name : str
    street: str
    city: str
    state: str
    zip: str
    lat: float
    lng: float

    # class Config():
    #     orm_mode = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Foo",
                "street": "M G Road",
                "city": "Banglore",
                "state": "Karntaka",
                "zip": "56006",
                "lat": "3.225",
                "lng": "5.4422",
            }
        }
