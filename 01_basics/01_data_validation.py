# 01_basics/01_data_validation.py

from pydantic import BaseModel, ValidationError
from typing import List


# --- 1. The Pydantic Blueprint ---
class AIModelData(BaseModel):
    """The contract for our data, inheriting Pydantic's validation magic."""

    name: str
    version: float  # Expects a float, will coerce "1.2" to 1.2
    models: List[str]  # Expects a list of strings


# --- 2. Good Data Example ---
good_data = {
    "name": "QueryBot 5000",
    "version": "1.2",  # Pydantic will convert this string to a float! (Coercion)
    "models": ["gpt-4", "claude-3"],
}

try:
    # Validation and object creation happen here!
    clean_object = AIModelData(**good_data)
    print("✅ Success! Data is clean and converted to an object.")
    print(f"Name: {clean_object.name}")
    print(f"Version type: {type(clean_object.version)}")

except ValidationError as e:
    print(f"❌ Unexpected Failure: {e}")


# --- 3. Bad Data Example (Missing Key) ---
bad_data_missing_key = {
    "name": "QueryBot 5000",
    # 'version' is missing and is required!
    "models": ["gpt-4"],
}

print("\n--- Testing Missing Key (Would cause KeyError without Pydantic) ---")
try:
    AIModelData(**bad_data_missing_key)
except ValidationError as e:
    # Pydantic gives a clean, clear error report
    print("❌ Validation Failed (Missing Key):")
    print(e.errors())
