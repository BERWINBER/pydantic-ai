# 03_complex_data/03_nested_models.py

from pydantic import BaseModel, Field, ValidationError
from typing import List


# --- BLUEPRINT 1: The Inner Model (The Object inside the list) ---
class ExtractedPerson(BaseModel):
    """Defines the structure for a single extracted entity."""

    name: str = Field(min_length=1)
    # Must be between 0.0 and 1.0
    confidence: float = Field(..., ge=0.0, le=1.0)


# --- BLUEPRINT 2: The Outer Model (The Wrapper) ---
class ExtractionResult(BaseModel):
    """Defines the overall structure, containing a list of inner models."""

    # This tells Pydantic to validate every item using the ExtractedPerson blueprint
    extracted_people: List[ExtractedPerson]


# --- Good Data (Fully Valid) ---
good_data = {
    "extracted_people": [
        {"name": "Alan Turing", "confidence": 0.99},
        {"name": "Grace Hopper", "confidence": 0.90},
    ]
}

try:
    result = ExtractionResult(**good_data)
    print("✅ Success! Nested data is clean.")
    print(f"First person's confidence: {result.extracted_people[0].confidence}")
except Exception as e:
    print(f"❌ Unexpected Failure: {e}")

# --- Bad Data (Error inside the list) ---
bad_data_nested_error = {
    "extracted_people": [
        {"name": "Ada Lovelace", "confidence": 0.85},
        # ERROR HERE: confidence is 1.2, breaking the le=1.0 rule!
        {"name": "Charles Babbage", "confidence": 1.2},
    ]
}

print("\n--- Testing Nested Error ---")
try:
    ExtractionResult(**bad_data_nested_error)
except ValidationError as e:
    print("❌ Validation Failed (Nested Error):")
    # Pydantic shows the exact path to the error: extracted_people -> index 1 -> confidence
    print(f"Error Location: {e.errors()[0]['loc']}")
    print(f"Error Message: {e.errors()[0]['msg']}")
