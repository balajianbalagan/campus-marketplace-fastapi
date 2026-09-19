from fastapi import FastAPI, Path, Query

app = FastAPI()

ROOMS = [
    {"building_id": 1, "room_number": "101", "capacity": 30, "has_projector": True},
    {"building_id": 1, "room_number": "102", "capacity": 12, "has_projector": False},
    {"building_id": 2, "room_number": "201", "capacity": 80, "has_projector": True},
]


# TODO: building_id must be an int greater than 0 (use Path(..., gt=0)).
@app.get("/buildings/{building_id}/rooms/{room_number}")
def get_room(building_id, room_number):
    raise NotImplementedError("TODO: implement get_room")


# TODO:
# - capacity_min: int | None = None -- only include rooms with capacity >= capacity_min
# - has_projector: bool = False -- if True, only include rooms with has_projector == True
# - limit: int = Query(10, le=50)
@app.get("/rooms")
def list_rooms():
    raise NotImplementedError("TODO: implement list_rooms")
