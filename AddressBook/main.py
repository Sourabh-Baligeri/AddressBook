import math
from urllib import request
from fastapi import FastAPI , Depends , Response, status, HTTPException,responses
from . import schemas , database , models
from . database import engine, SessionLocal
from sqlalchemy.orm import Session 

app = FastAPI()

#for Create model Address
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Welcome Msg Displaying in Front Page of The Application
@app.get("/")
def index():
    return {"AddressBook": "Welcome To AddressBook Application"}

# Fetching All The Records and Displaying
@app.get("/addresses/")
def all(db : Session = Depends(get_db)):
    address = db.query(models.Address).all()
    return address

# Create Addresses Method
@app.post('/addresses/', response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create(request :schemas.Address , db : Session = Depends(get_db)):
    address = models.Address(**request.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

# Get Single User Address
@app.get('/address/{id}')
def get_address(id, db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Address With The id {id} is Not Avalable")
    return address

#Delete the Address
@app.delete('/address/{id}')
def destroy(id, db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Address With The id {id} is Not Avalable")
    db.delete(address)
    db.commit()
    return {"Message":"Address Deleted Successfully"}

# Edit The Address
@app.put('/addresse/{id}', response_model=schemas.Address,status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Address,db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Address With The id {id} is Not Avalable")
    address.name = request.name
    address.street = request.street
    address.city = request.city
    address.state = request.state
    address.zip = request.zip
    address.lat = request.lat
    address.lng = request.lng
    db.commit()
    return address

# Get The address with coordinates 
@app.get('/address/{lat}/{lng}')
def get_coordinates(lat: float, lng: float, db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.lat <= lat, models.Address.lng <= lng).all()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"The Given Coordinates With The lat: {lat} and  lng: {lng} are Not Avalable in Records")
    return address

# Get the Coordinates with near usingg Radious
@app.get('/addresses/{lat}/{lng}/{radius}')
def get_address_by_coordinates(lat: float, lng: float, radius: float,db : Session = Depends(get_db)):
    print("Record",lat,lng)
    radi = 6371
    dblat = db.query(models.Address).all()
    for a in dblat:
        # print("ALL:",a.lat, a.lng)
        
        dlat = math.radians(lat - float(a.lat))
        dlon = math.radians(lng - float(a.lng))
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(float(a.lat))) \
            * math.cos(math.radians(float(a.lat))) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radi * c        
        if d <= radius:
            return d
        else:
            return "No Records Found, Please Try Again"
    return d
