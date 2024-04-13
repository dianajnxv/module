from typing import Union, Optional
from http.client import HTTPException
from app import models
from app import schemes

from sqlalchemy.orm import Session

import hashlib


def create_user(db: Session, user: schemes.UserCreate) -> schemes.User:
    hashed_password = hashlib.md5(user.password.encode())
    db_user = models.User(email=user.email, first_name=user.first_name,
                          second_name=user.second_name, password=hashed_password.hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_record(db: Session, item: schemes.RecordCreate, user_id: int) -> schemes.Record:
    db_record = models.Record(**item.dict(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_user(db: Session, user_id: int) -> Optional[schemes.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user: schemes.User) -> schemes.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.email:
        db_user.email = user.email
    if user.first_name:
        db_user.first_name = user.first_name
    if user.second_name:
        db_user.second_name = user.second_name
    if user.password:
        hashed_password = hashlib.md5(user.password.encode())
        db_user.password = hashed_password.hexdigest()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_record(db: Session, record_id: int) -> models.Record:
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def delete_record(db: Session, record_id: int) -> models.Record:
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return db_record
    else:
        raise HTTPException(status_code=404, detail="Record not found")


def update_record(db: Session, record_id: int, record: schemes.Record) -> schemes.Record:
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.title:
        db_record.title = record.title
    if record.content:
        db_record.content = record.content
    db.commit()
    db.refresh(db_record)
    return db_record
