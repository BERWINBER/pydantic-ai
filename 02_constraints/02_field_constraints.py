# 02_constraints/02_field_constraints.py

from pydantic import BaseModel, Field, ValidationError


class ClassificationResult(BaseModel):
    # Field 1: Must be a float, Greater than or Equal to 0 and Less than or Equal to 1.
    probability: float = Field(..., ge=0.0, le=1.0)

    # Field 2: Must be a string, Minimum length of 3 characters.
    result_name: str = Field(..., min_length=3)

    # Field 3: Optional field, but if present, must be >= 1.
    category_id: int | None = Field(default=None, ge=1)


# --- Failure Case 1: Probability out of range ---
invalid_prob = {
    "probability": 1.2,  # Breaks the le=1.0 rule
    "result_name": "OK",
}

try:
    ClassificationResult(**invalid_prob)
except ValidationError as e:
    print("❌ Failed: Probability is > 1.0")
    print(e.errors()[0]["msg"])

# --- Failure Case 2: Name too short ---
invalid_name = {
    "probability": 0.8,
    "result_name": "A",  # Breaks the min_length=3 rule
}

try:
    ClassificationResult(**invalid_name)
except ValidationError as e:
    print("\n❌ Failed: Name is too short")
    print(e.errors()[0]["msg"])
