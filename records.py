from app import schemes, crud
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

records_router = APIRouter(prefix="/records", tags=["records"])


@records_router.post("/", response_model=schemes.Record)
def create_user_record(record: schemes.RecordCreate, db: Session = Depends(get_db)) -> schemes.Record:
    db_user = crud.get_user_by_email(db, email=record.user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with email {record.user_email} not found")
    db_record = crud.create_user_record(db, item=record, user_id=db_user.id)
    return db_record


@records_router.get("/{record_id}", response_model=schemes.Record)
def read_user_record(record_id: int, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record


@records_router.put("/{record_id}", response_model=schemes.Record)
def update_user_record(record_id: int, record: schemes.Record, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return crud.update_record(db, record_id=record_id, record=record)


@records_router.delete("/{record_id}", response_model=schemes.Record)
def delete_user_record(record_id: int, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return crud.delete_record(db, record_id=record_id)
