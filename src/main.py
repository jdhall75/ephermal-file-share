import mimetypes
import os
import random
import shutil
import string
import time

from fastapi import BackgroundTasks, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

# create tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# setup the app
base_url = "http://127.0.0.1:8080"
upload_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads")
app = FastAPI()


def rand_string(length: int = 8) -> str:
    values = string.ascii_lowercase + string.digits
    return "".join([random.choice(values) for n in range(length)])


def cleanup_file(db: Session, db_file: models.UploadFiles):
    time.sleep(30)
    # delete the file
    os.unlink(f"{upload_dir}/{db_file.name}")
    # remove it from the db
    db.delete(db_file)
    db.commit()


@app.get("/{key}")
def pickup_file(key: str, bt: BackgroundTasks, db: Session = Depends(get_db)):
    # query the database for the key return file name
    # send the file with size and mime type..
    print(key)
    db_file = crud.get_file_by_key(db, key)
    if db_file is None:
        return HTTPException(404)
    file_path = f"{upload_dir}/{db_file.name}"
    mime_type = mimetypes.guess_type(file_path)[0]
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as fp:
        bt.add_task(cleanup_file, db, db_file)
        return StreamingResponse(
            fp, media_type=mime_type, headers={"content-length": str(file_size)}
        )
    


@app.post("/")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(f"{upload_dir}/{file.filename}", "wb+") as upload:
        shutil.copyfileobj(file.file, upload)
    key = rand_string()
    file.file.close()
    crud.insert_file(db, str(file.filename), key)
    return {
        "file_name": file.filename,
        "url": "".join([base_url, "/", key]),
        "key": key,
    }
