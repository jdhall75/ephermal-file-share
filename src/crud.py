from sqlalchemy.orm import Session

from . import models


def get_file_by_key(db: Session, key: str):
    return db.query(models.UploadFiles).filter(models.UploadFiles.key == key).first()


def insert_file(db: Session, filename: str, key: str):
    db_file = models.UploadFiles(name=filename, key=key)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, id: int):
    db_file = db.query(models.UploadFiles).filter(models.UploadFiles.id == id).first()
    db.delete(db_file)
    db.commit()


def delete_file_by_key(db: Session, key: str):
    db_file = db.query(models.UploadFiles).filter(models.UploadFiles.key == key).first()
    db.delete(db_file)
    db.commit()
