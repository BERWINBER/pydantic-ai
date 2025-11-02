# 05_output_export/05_data_export.py

from pydantic import BaseModel
from typing import List


# Define a simple model
class APIResponseData(BaseModel):
    status: str
    code: int
    data: List[int]


# Create a validated Pydantic object
response_obj = APIResponseData(status="success", code=200, data=[42, 101, 99])

print(f"Initial Object Type: {type(response_obj)}")

# --- METHOD 1: Export to Dictionary (.model_dump()) ---
data_dict = response_obj.model_dump()

print("\n--- Exported to Python Dictionary ---")
print(data_dict)
print(f"Type: {type(data_dict)}")

# --- METHOD 2: Export to JSON String (.model_dump_json()) ---
json_string = response_obj.model_dump_json()

print("\n--- Exported to JSON String ---")
print(json_string)
print(f"Type: {type(json_string)}")
