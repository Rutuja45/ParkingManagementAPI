from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from .. import models, schemas, database, auth

router = APIRouter(prefix="/parking", tags=["Parking Slots"])



@router.post("/slots/create", response_model=schemas.ParkingSlotOut)
def create_slot(slot: schemas.ParkingSlotCreate,
               db: Session = Depends(database.get_db),
               current_user: models.User = Depends(auth.get_admin_user)):
   new_slot = models.ParkingSlot(
       location=slot.location,
       slot_number=slot.slot_number,
       floor=slot.floor  # NEW FIELD
   )
   db.add(new_slot)
   db.commit()
   db.refresh(new_slot)
   return new_slot


@router.get("/slots", response_model=List[schemas.ParkingSlotOut])
def get_slots(floor: Optional[int] = None,
             db: Session = Depends(database.get_db)):
   query = db.query(models.ParkingSlot)
   if floor is not None:
       query = query.filter(models.ParkingSlot.floor == floor)
   return query.all()


@router.put("/{slot_id}")
def update_slot(slot_id: int, in_maintenance: bool, db: Session = Depends(database.get_db),
                admin_user: models.User = Depends(auth.get_admin_user)):
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    slot.in_maintenance = in_maintenance

    db.commit()

    return {"message": "Slot updated"}


@router.delete("/{slot_id}")
def delete_slot(slot_id: int, db: Session = Depends(database.get_db)):
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    db.delete(slot)

    db.commit()

    return {"message": "Slot deleted"}
