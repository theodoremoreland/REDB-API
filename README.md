# REDB API (Abridged)
An asynchronous REST API for accessing St. Louis Parcel Data stored in the Regional Entity Database (REDB). 

This repository features an abridged version of the actual REDB-API, the actual repository can be found here: https://github.com/stlrda/redb-api  

More information on the Regional Entity Database can be found here: https://github.com/stlrda/REDB-Workflows  

REDB-API is a public facing API that comes equipped with interactive documentation thanks to the Fast-API library. Said documentation can be utilized by anyone over the internet either programatically or through a web browser. Below is a demonstration of using the point-and-click web interface to preview and retrieve data from the Regional Entity Database.


## Home Screen Preview #1
<img src="presentation/1.PNG" width="900">

## Home Screen Preview #2
<img src="presentation/2.PNG" width="900">

## Queries Screen Preview #1
<img src="presentation/3.PNG" width="900">

## Inputting the name "Theodore" for Legal Entity data
<img src="presentation/4.PNG" width="900">

## Legal Entity data returned from input "Theodore"
<img src="presentation/5.PNG" width="900">

## You can download the JSON returned from queries
<img src="presentation/6.PNG" width="600">

## Grabbing the same Legal Entity data by id
<img src="presentation/7.PNG" width="900">

## Getting Parcel data for given Legal Entity ID
<img src="presentation/8.PNG" width="900">

## Getting Parcel data from a REDB parcel_id
<img src="presentation/9.PNG" width="900">

## Parcel data returned after submitting address: 4921 THEKLA AV
<img src="presentation/10.PNG" width="900">

## Building counts for Parcels of a certain kind (in this case, those in Ward 9)
<img src="presentation/11.PNG" width="900">

## Parcel IDs for all Parcels of a certain kind (in this case, those in Ward 9)
<img src="presentation/12.PNG" width="900">

## Retrieving an excessive amount of data for a Parcel by the handle 10097000030
<img src="presentation/13.PNG" width="900">

## See the last time REDB was updated
<img src="presentation/14.PNG" width="900">

## Routes and Query Parameters
* /redb/parcel/redb_id
  This endpoint returns json which contain information about the parcel(s), building(s), and unit(s) related to a parcel id.<br><br>
  The redb_id endpoint requires two inputs for a get request.<br>
  - {ParcelInput: str} - Input the full redb parcel id that you want to search the database for<br>
  - {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>


* /redb/parcel/legal_entity_id
  This endpoint returns json which contain information about the parcel(s), building(s), and unit(s) related to a legal_entity_id.<br><br>
  The legal_entity_id endpoint requires two inputs for a get request.<br>
  - {IdInput: str} - Input the legal_entity_id that you want to search the database for<br>
  - {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

* /redb/parcel/adddress
  This endpoint returns json which contain information about the parcel(s), building(s), and unit(s) related to a street address.<br><br>
  The address endpoint requires two inputs for a get request.<br>
  - {AddressInput: str} - Input the address that you want to search the database for<br>
  - {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

  The address end point uses trigrams and fuzzy matching in order to return all the information related to an address in the database that most closely matches the AddressInput.<br>

* /redb/legal_entity/name
  This endpoint returns json which contain information about legal entities within the database based on a name.<br><br>
  The name endpoint requires a single input for a get request.<br>
  - {NameInput: str} - Input the legal_entity_name that you want to search the database for<br>

  The name endpoint uses trigrams and fuzzy matching in order to return all of the legal entity records whose legal_entity_name field is similar to the NameInput.  The output returned by the end point is ordered such that the closest matches are listed first so being more specific should help you find the desired legal_entity faster.  Legal Names are entered in Lastname, Firstname format.

* /readb/filter/counts
  This endpoint returns json which contain counts of the commercial use and residential use buildings located on parcels that match the selected criteria.<br><br>
  The counts endpoint requires two inputs for a get request.<br>
  - {FilterTypeInput: str} - The field you would like to filter on<br>
  - {FilterValueInput: str} - The value of the filter field you want to filter on<br>

  The acceptable criteria for the FileTypeInput field are as follows:<br>
  [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]<br>

* /readb/filter/ids
  This endpoint returns json which contain the parcel_ids of all the parcels that match the selected criteria.<br><br>
  The ids endpoint requires two inputs for a get request.<br>
  - {FilterTypeInput: str} - The field you would like to filter on<br>
  - {FilterValueInput: str} - The value of the filter field you want to filter on<br>

  The acceptable criteria for the FileTypeInput field are as follows:<br>
  [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]<br>

* /redb/parcel_detail
  This endpoint returns an excess of information concerning a particular parcel identified by government "handle"
  - {handle: int}

* /redb/latest
  This endpoint returns json containing the date of the most recent update in redb.<br>