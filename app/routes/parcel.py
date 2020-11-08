# Third party
from fastapi import APIRouter

# Custom
from app.routes import ParcelInfo
from app.routes import database

router = APIRouter()

@router.get('/redb/parcel/redb_id', response_model=ParcelInfo)
async def Find_Parcel_By_REDB_Id(ParcelInput: str, Current: bool):
    """This endpoint returns json which contains information about the parcel(s), building(s), and unit(s) related to a parcel id.
    """

    values = {'ParcelId': ParcelInput}

    if Current == True:
        current_flag_select = ''
        current_flag_where = 'AND current_flag = TRUE'
        current_flag_parcel_select = ''
        current_flag_parcel_where = 'AND parcel.current_flag = TRUE'
    else:
        current_flag_select = ', current_flag'
        current_flag_where = ''
        current_flag_parcel_select = ', parcel.current_flag'
        current_flag_parcel_where = ''

    query_parcels = f'''SELECT parcel_id
                        , parcel.county_id
                        , CONCAT(address.street_address, ' ', address.city, ' ', address.state, ' ', address.country, ' ', address.zip) AS address
                        , city_block_number
                        , parcel_number
                        , owner_id
                        , description
                        , frontage_to_street
                        , land_area
                        , zoning_class
                        , ward
                        , voting_precinct
                        , inspection_area
                        , neighborhood_id
                        , police_district
                        , census_tract
                        , asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , gis_city_block
                        , gis_parcel
                        , gis_owner_code
                        {current_flag_parcel_select}
                    FROM "core"."parcel"
                    JOIN "core"."address"
                    ON "address"."address_id" = "parcel"."address_id"
                    LEFT JOIN "core"."special_parcel_type"
                    ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE("parcel"."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                    ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE("parcel"."sub_parcel_type_code", 'null')
                    WHERE parcel_id = :ParcelId
                    {current_flag_parcel_where}'''
    
    query_buildings = f'''SELECT building_id
                        , owner_id
                        , description
                        , building_use
                        , apartment_count
                        {current_flag_select}
                    FROM "core"."building" 
                    WHERE CONCAT(SUBSTRING(building_id FROM 1 FOR 14), \'.000.0000\') = :ParcelId
                    {current_flag_where}'''
    
    query_units = f'''SELECT unit_id
                        , owner_id
                        , description
                        , condominium
                        {current_flag_select}
                    FROM "core"."unit" 
                    WHERE CONCAT(SUBSTRING(unit_id FROM 1 FOR 14), \'.000.0000\') = :ParcelId
                    {current_flag_where}'''

    parcel_info_dict = await database.fetch_all(query=query_parcels, values=values)
    building_info_dict = await database.fetch_all(query=query_buildings, values=values)
    unit_info_dict = await database.fetch_all(query=query_units, values=values)

    combined_dict = {'parcels':parcel_info_dict,'buildings':building_info_dict,'units':unit_info_dict}
    return combined_dict


@router.get('/redb/parcel/legal_entity_id', response_model=ParcelInfo)
async def Find_Parcels_By_Legal_Entity_Id(IdInput: str, Current:bool):
    """This endpoint returns json which contains information about the parcel(s), building(s), and unit(s) related to a legal_entity_id.
    If you don't know the legal_entity_id of a person or business try looking it up by using the /redb/legal_entity/name endpoint first.
    """

    values = {'Legal_Entity_Id': IdInput}

    if Current == True:
        current_flag_select = ''
        current_flag_where = 'AND current_flag = TRUE'
        current_flag_parcel_select = ''
        current_flag_parcel_where = 'AND parcel.current_flag = TRUE'
    else:
        current_flag_select = ', current_flag'
        current_flag_where = ''
        current_flag_parcel_select = ', parcel.current_flag'
        current_flag_parcel_where = ''

    query_parcels = f'''SELECT parcel_id
                        , parcel.county_id
                        , CONCAT(address.street_address, ' ', address.city, ' ', address.state, ' ', address.country, ' ', address.zip) AS address
                        , city_block_number
                        , parcel_number
                        , owner_id
                        , description
                        , frontage_to_street
                        , land_area
                        , zoning_class
                        , ward
                        , voting_precinct
                        , inspection_area
                        , neighborhood_id
                        , police_district
                        , census_tract
                        , asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , gis_city_block
                        , gis_parcel
                        , gis_owner_code
                        {current_flag_parcel_select}
                    FROM "core"."parcel"
                    JOIN "core"."address"
                    ON "address"."address_id" = "parcel"."address_id"
                    LEFT JOIN "core"."special_parcel_type"
                    ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE("parcel"."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                    ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE("parcel"."sub_parcel_type_code", 'null')
                    WHERE owner_id = :Legal_Entity_Id
                    {current_flag_parcel_where}'''
    
    query_buildings = f'''SELECT building_id
                        , owner_id
                        , description
                        , building_use
                        , apartment_count
                        {current_flag_select}
                        FROM core.building 
                        WHERE owner_id = :Legal_Entity_Id
                        {current_flag_where}
                        ORDER BY building.building_id'''
    
    query_units = f'''SELECT unit_id
                        , owner_id
                        , unit.description
                        , condominium
                        {current_flag_select}
                        FROM core.unit 
                        WHERE owner_id = :Legal_Entity_Id
                        {current_flag_where}'''

    parcel_info_dict = await database.fetch_all(query=query_parcels, values=values)
    building_info_dict = await database.fetch_all(query=query_buildings, values=values)
    unit_info_dict = await database.fetch_all(query=query_units, values=values)

    combined_dict = {'parcels':parcel_info_dict,'buildings':building_info_dict,'units':unit_info_dict}
    return combined_dict


@router.get('/redb/parcel/address', response_model=ParcelInfo)
async def Find_Parcels_By_Address(AddressInput: str, Current: bool):
    """This route returns parcel data for a given address. The parcel data includes
    parcel(s) from the "core.parcel" table as well as each building and unit associated with
    said parcel(s).
    """

    values = {'address': AddressInput}
    address_subquery = '''
                        (
                        SELECT
                            address_id
                        FROM "core"."address"
                        WHERE
                            SIMILARITY(CONCAT(street_address, ' ', city, ' ', address.state, ' ', country, ' ', zip), :address) > 0.4
                        ORDER BY
                            WORD_SIMILARITY(CONCAT(street_address, ' ', city, ' ', address.state, ' ', country, ' ', zip), :address) DESC
                        LIMIT 1
                        )
                        '''

    parcel_where = f'WHERE p.address_id = {address_subquery} AND p.current_flag = TRUE' if Current else f'WHERE p.address_id = {address_subquery}'

    query_parcels = f'''
                    SELECT 
                        p.parcel_id
                        , p.county_id
                        , CONCAT(a."street_address", ' ', a."city", ' ', a."state", ' ', a."country", ' ', a."zip") as address
                        , p.city_block_number
                        , p.parcel_number
                        , p.owner_id
                        , p.description
                        , p.frontage_to_street
                        , p.land_area
                        , p.zoning_class
                        , p.ward
                        , p.voting_precinct
                        , p.inspection_area
                        , p.neighborhood_id
                        , p.police_district
                        , p.census_tract
                        , p.asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , p.gis_city_block
                        , p.gis_parcel
                        , p.gis_owner_code
                        , p.create_date
                        , p.current_flag
                    FROM "core"."parcel" p
                    LEFT JOIN "core"."special_parcel_type"
                        ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE(p."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                        ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE(p."sub_parcel_type_code", 'null')
                    JOIN "core"."address" a
                        ON p."address_id" = a."address_id"
                    {parcel_where}
                    ;
                    '''

    # Filtering buildings and units by a given parcel's parcel_id, current_flag, and create date is to ensure
    # that the buildings and units correspond to the exact instance of the parcel. parcel_id alone is not
    # sufficient because a parcel with an updated address and thus multiple instances of the same parcel_id
    # can have buildings and units that correspend to that instance specifically, but not to previous instances.
    # If we're assuming that only one instance of a parcel_id appears in parcels on a given date, the current_flag
    # and create_date will distinguish the buildings and units that only correspond to the parcel_id from the
    # buildings and units that also correspond to the given address.
    
    # Fetch parcel data for given address.
    parcels_fetch = await database.fetch_all(query=query_parcels, values=values) 
    # Assign fetched parcel_ids, current_flags, and create_dates to variables.
    parcel_ids = [parcel['parcel_id'] for parcel in parcels_fetch]
    parcel_ids_and_current_flags = [parcel['parcel_id'] + str(parcel["current_flag"]).lower() for parcel in parcels_fetch]
    parcel_create_dates = [parcel['create_date'].strftime("%Y-%m-%d") for parcel in parcels_fetch]
    
    if len(parcels_fetch) == 0:
        return {'parcels':[], 'buildings':[], 'units':[]}

    
    if Current:
        buildings_where = f'WHERE "current_flag" = True AND "parcel_id" = ANY(ARRAY{parcel_ids})'
        units_where = f'WHERE u."current_flag" = True AND "parcel_id" = ANY(ARRAY{parcel_ids})'
    else:
        buildings_where = f'''
                            WHERE
                                CONCAT("parcel_id", "current_flag"::text) = ANY(ARRAY{parcel_ids_and_current_flags})
                            AND CAST("create_date" as VARCHAR) = ANY(ARRAY{parcel_create_dates})
                          '''  

        units_where = f'''
                        WHERE
                            CONCAT(p."parcel_id", u."current_flag"::text) = ANY(ARRAY{parcel_ids_and_current_flags})
                        AND CAST(u."create_date" as VARCHAR) = ANY(ARRAY{parcel_create_dates})
                      '''

    query_buildings = f'''
                        SELECT 
                            building_id
                            , owner_id
                            , description
                            , building_use
                            , apartment_count
                            , create_date
                            , current_flag
                        FROM "core"."building"
                        {buildings_where}
                        ;
                        '''
    
    query_units = f'''
                    SELECT 
                        u.unit_id
                        , u.owner_id
                        , u.description
                        , u.condominium
                        , u.create_date
                        , u.current_flag
                    FROM "core"."unit" u
                    JOIN "core"."parcel" p
                        ON SUBSTRING(u."unit_id" FROM 1 FOR 14) = SUBSTRING(p."parcel_id" FROM 1 FOR 14)
                    {units_where}
                    ;
                    '''

    parcel_info_list = parcels_fetch
    # Fetch buildings and units that correspond to each parcel's parcel_id, current_flag, and create date.
    building_info_list = await database.fetch_all(query=query_buildings)
    unit_info_list = await database.fetch_all(query=query_units)

    parcels_by_address_dict = {'parcels':parcel_info_list, 'buildings':building_info_list, 'units':unit_info_list}
    return parcels_by_address_dict # Return a dictionary containing a list of each parcel, building, and unit related to given address.