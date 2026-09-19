# Exercise: Request Body Validation & Nested Models

Build a "study group signup" endpoint that exercises Pydantic body validation, nested
models, and proper error handling.

## Task (`starter/main.py`)

Define `TimeSlot` (nested model: `day: str`, `start_hour: int` 0-23, `end_hour: int` 0-23,
`end_hour` must be greater than `start_hour`) and `StudyGroupCreate` (`course_code: str`
min length 2, `max_members: int` between 2 and 12, `slots: list[TimeSlot]` at least 1 slot).

`POST /study-groups` — validate and echo back `{"course_code": ..., "max_members": ...,
"slot_count": len(slots)}`, `201`. If `end_hour <= start_hour` for any slot, respond `400`
with `detail` mentioning which day is invalid (don't rely on the built-in 422 for this one —
it's cross-field, so validate it yourself in the endpoint after Pydantic's own checks pass).

## Run

```bash
cd starter
python -m pytest ../tests -v
```
