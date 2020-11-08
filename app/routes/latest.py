# Third party
from fastapi import APIRouter

# Custom
from app.routes import database

router = APIRouter()

@router.get('/redb/latest')
async def Find_Latest_Update():
    """This endpoint returns json which contains the date that REDB was last updated.
    """

    query = '''WITH LATEST_UPDATE AS
            (
                SELECT MAX("update_date") as "update_date" FROM "core"."neighborhood"
                UNION
                SELECT MAX("update_date") as "update_date" FROM  "core"."address"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."county_id_mapping_table"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."legal_entity"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."parcel"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."building"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."unit"
            )
            SELECT MAX("update_date") as "update_date" FROM LATEST_UPDATE'''
    return await database.fetch_one(query=query)