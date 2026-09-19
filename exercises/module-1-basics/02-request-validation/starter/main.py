from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


# TODO: day: str, start_hour: int (ge=0, le=23), end_hour: int (ge=0, le=23)
class TimeSlot(BaseModel):
    ...


# TODO: course_code: str (min_length=2), max_members: int (ge=2, le=12),
# slots: list[TimeSlot] (min_length=1)
class StudyGroupCreate(BaseModel):
    ...


@app.post("/study-groups", status_code=201)
def create_study_group(group: StudyGroupCreate):
    # TODO: for each slot in group.slots, if slot.end_hour <= slot.start_hour, raise
    # HTTPException(400, detail=f"Invalid time slot on {slot.day}: end_hour must be after start_hour")
    # Then return {"course_code": ..., "max_members": ..., "slot_count": len(group.slots)}
    raise NotImplementedError("TODO: implement create_study_group")
