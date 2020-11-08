# Third party
from fastapi import APIRouter, HTTPException

# Custom
from app.routes import FilterParcelCounts, FilterParcelIds, List
from app.routes import database

router = APIRouter()

# Return counts of bus/res buildings by filter #
@router.get('/redb/filter/counts', response_model = List[FilterParcelCounts])
async def Building_Counts_By_Filter(FilterTypeInput: str, FilterValueInput: str):
    """This endpoint returns json which contains counts of the commercial use and residential use buildings located on parcels that match the selected criteria.
    """
    
    values = {'FilterValue': FilterValueInput}
    allowedFliters = ['zoning_class', 'ward', 'voting_precinct', 'inspection_area', 'neighborhood_id', 'police_district', 'census_tract']

    if FilterTypeInput in allowedFliters:
        query = f'''SELECT DISTINCT building_use, COUNT(*)
                    FROM core.building
                    JOIN (SELECT parcel_id, {FilterTypeInput} FROM core.parcel WHERE {FilterTypeInput} = :FilterValue AND current_flag = TRUE) Parcel_Filter
                    ON Parcel_Filter.parcel_id = building.parcel_id
                    GROUP BY building_use
                    HAVING "building_use" IN ('COM','RES')
                    '''
        building_counts = await database.fetch_all(query=query, values=values)        
        return building_counts
    else:
        raise HTTPException(status_code=400, detail='Unsupported filter. Please use one of the following: [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]')


# Return all current parcel ids by filter #
@router.get('/redb/filter/ids', response_model = List[FilterParcelIds])
async def Building_IDs_By_Filter(FilterTypeInput: str, FilterValueInput: str):
    """This endpoint returns json which contains the parcel_ids of all the parcels that match the selected criteria.
    """

    values = {'FilterValue': FilterValueInput}
    allowedFliters = ['zoning_class', 'ward', 'voting_precinct', 'inspection_area', 'neighborhood_id', 'police_district', 'census_tract']

    if FilterTypeInput in allowedFliters:
            query = f'''SELECT DISTINCT parcel_id 
                    FROM core.parcel 
                    WHERE {FilterTypeInput} = :FilterValue 
                    AND current_flag = TRUE'''
            parcelIDs = await database.fetch_all(query=query, values=values)        
            return parcelIDs
    else:
        raise HTTPException(status_code=400, detail='Unsupported filter. Please use one of the following: [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]')
