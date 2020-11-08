# Third party
from fastapi import APIRouter

# Custom
from app.routes import LegalEntity, List
from app.routes import database

router = APIRouter()

@router.get('/redb/legal_entity/name', response_model=List[LegalEntity])
async def Find_Legal_Entity_By_Name(nameInput: str):
    """This endpoint returns json which contains information about legal entities within the database based on a name.
    """

    query = f'''SELECT * 
                FROM "core"."legal_entity"
                WHERE SIMILARITY(legal_entity_name, :name) > 0.4
                ORDER BY WORD_SIMILARITY("legal_entity_name", :name) DESC'''
    values = {'name': nameInput}
    legal_entities = await database.fetch_all(query=query, values=values)
    return legal_entities


@router.get('/redb/legal_entity/id', response_model=List[LegalEntity])
async def Find_Legal_Entity_By_Id(IdInput: int):
    """This endpoint returns json which contains information about legal entities within the database based on an id.
    """

    query = f'''SELECT * 
                FROM "core"."legal_entity"
                WHERE legal_entity_id = :legal_entity_id
            '''
    values = {'legal_entity_id': IdInput}
    legal_entities = await database.fetch_all(query=query, values=values)
    return legal_entities