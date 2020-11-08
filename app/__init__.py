# Third party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse

# Custom
from .routes import (
    database
    , engine
    , parcel
    , legal_entity
    , parcel_detail
    , _filter
    , latest
)

app = FastAPI(title='REDB API', docs_url="/redb/docs", redoc_url="/redb/redoc", openapi_url="/redb/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=['*'])
app.include_router(parcel.router)
app.include_router(parcel_detail.router)
app.include_router(legal_entity.router)
app.include_router(latest.router)
app.include_router(_filter.router)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# Redirect Root to Docs 
@app.get('/redb')
async def get_api_docs():
    response = RedirectResponse(url='/redb/redoc')
    return response


def api_docs():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title='Regional Entity Database',
        version='0.1.0',
        description='Automatically Updated, land parcel data from Saint Louis, provided by the St. Louis Regional Data Alliance .<br><br>If you\'d prefer to interact with queries in browser, see the <a href=\'/redb/docs\'>Swagger UI</a>',
        routes=app.routes,#[13:], # Need to Verify this to Obfuscate Some Routes from Docs
        #openapi_prefix=openapi_prefix
    )
    openapi_schema['info']['x-logo'] = {
        'url' : 'https://stldata.org/wp-content/uploads/2019/06/rda-favicon.png' # Need a more permanent source
    }
    app.openapi_schema = openapi_schema
    
    return app.openapi_schema

app.openapi = api_docs

