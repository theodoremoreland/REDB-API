# Native
import json

# Third party
from fastapi import APIRouter

# Custom
from app.routes import database

router = APIRouter()

@router.get('/redb/parcel_detail')
async def parcel_detail(handle: str):
    """This endpoint returns json which contains an excess of information for a parcel.
    """

    query = 'SELECT parcel_data FROM "city_api"."parcel_data" WHERE handle = :handle;'
    values = {'handle': handle}
    data = await database.fetch_one(query=query, values=values)
    return json.loads(dict(data)['parcel_data'])