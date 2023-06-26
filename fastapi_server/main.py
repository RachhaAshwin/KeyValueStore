import os
import json
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from db import DB

app = FastAPI()
database = DB(os.environ.get('DB_FILE_PATH') or 'kv.db')


@app.get("/")
def read_root():
    return {'database': json.loads(database.dumps())}


@app.get('/get')
def db_get(key: str):
    if not key:
        raise HTTPException(status_code=400, detail="Missing parameter 'key'")
    return {'key': key, 'value': database.get(key)}

@app.post('/set')
async def db_set(key: str, value: str):
    try:
        #body = await request.json()
        #key = body.get('key')
        #value = body.get('value')
        if not key:
            raise HTTPException(status_code=400, detail="Missing parameter 'key'")
        if not value:
            raise HTTPException(status_code=400, detail="Missing parameter 'value'")
        result = database.set(key, value)
        print(result)
        if result:
            return {'message': f"Key '{key}' set to Value '{value}'"}
        else:
            return JSONResponse(status_code=400, content={'error': f"There was a problem saving ({key}, {value}) to the DB."})
    except Exception:
        return JSONResponse(status_code=422, content={'error': 'Unable to process this request.'})

@app.delete('/remove/{key}')
def db_remove(key: str):
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Missing parameter 'key'")
        try:
            result = database.remove(key)
        except KeyError as key_err:
            raise HTTPException(status_code=404, detail=str(key_err)[1:-1])
        if result:
            return {'message': f"Key '{key}' removed from DB."}
        else:
            return JSONResponse(status_code=400, content={'error': f"There was a problem removing Key '{key}' from the DB."})
    except Exception:
        return JSONResponse(status_code=422, content={'error': f"Unable to process this request. Details: {traceback.format_exc()}"})


@app.get('/keys')
def db_keys():
    return {'keys': list(database.keys())}

@app.get('/values')
def db_values():
    return {'values': list(database.values())}

@app.get('/items')
def db_items():
    return {'items': [list(item) for item in database.items()]}

@app.get('/dumps')
def db_dumps():
    return {'database': json.loads(database.dumps())}

@app.post('/truncate-db')
def db_truncate():
    result = database.truncate_db()
    if result:
        return {'message': 'DB has been truncated successfully.'}
    else:
        return JSONResponse(status_code=400, content={'error': 'There was a problem truncating the DB.'})
