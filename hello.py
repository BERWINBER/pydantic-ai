from pydantic import BaseModel, ValidationError, Field
from typing import List


def process_model_data(data: dict):
    # We hope the 'name' key exists...
    print(f"Processing model: {data['name']}")

    # We hope 'version' is a number so we can do math...
    if data["version"] > 1.0:
        print("This is a new version!")

    # We hope 'models' is a list so we can loop...
    for model in data["models"]:
        print(f"- {model}")


# ---
# This data is perfect. Everything works.
good_data = {"name": "QueryBot 5000", "version": 1.2, "models": ["gpt-4", "claude-3"]}
process_model_data(good_data)

# 'version' key is missing!
bad_data_1 = {"name": "QueryBot 5000", "models": ["gpt-4"]}
# process_model_data(bad_data_1)
# CRASH! -> KeyError: 'version'
# 'version' is a string, not a number!
bad_data_2 = {
    "name": "QueryBot 5000",
    "version": "1.2",  # This is a string!
    "models": ["gpt-4"],
}
# process_model_data(bad_data_2)
# CRASH! -> TypeError: '>' not supported between 'str' and 'float'


# We create a class that is our "blueprint"
# It inherits from BaseModel, which gives it all the magic.
class AIModelData(BaseModel):
    name: str  # The 'name' field MUST be a string (str)
    version: float  # The 'version' field MUST be a float (float)
    models: List[str]


good_data = {"name": "QueryBot 5000", "version": 1.2, "models": ["gpt-4", "claude-3"]}
# Let's try to create an instance of our blueprint
# Pydantic checks it.
model_object = AIModelData(**good_data)  # The ** unpacks the dictionary
print("✅ Success! Data is valid.")
print(f"Name from object: {model_object.name}")
print(f"Version from object: {model_object.version}")
data_with_string_version = {
    "name": "QueryBot 5000",
    "version": "1.2",  # This is a string!
    "models": ["gpt-4"],
}  # Pydantic is smart! It sees "1.2" and knows you want a float.
# It automatically converts (coerces) the string to a float.
model_object_2 = AIModelData(**data_with_string_version)
print(f"\n✅ Pydantic auto-converted the version!")
print(f"The version is: {model_object_2.version}")
print(f"The type is: {type(model_object_2.version)}")  # -> <class 'float'>
# Your program is saved!

# 'version' is completely missing
bad_data_1 = {"name": "QueryBot 5000", "models": ["gpt-4"]}

try:
    AIModelData(**bad_data_1)
except ValidationError as e:
    print("\n❌ Pydantic caught the error (Missing Data):")
    # It gives you a beautiful, clear error message
    print(e)
    # Output:
    # 1 validation error for AIModelData
    # version
    #   Field required [type=missing, ...]

# ---
# 'models' is the wrong type (a string, not a list)
bad_data_3 = {
    "name": "QueryBot 5000",
    "version": 1.5,
    "models": "gpt-4, claude-3",  # This is just one string
}

try:
    AIModelData(**bad_data_3)
except ValidationError as e:
    print("\n❌ Pydantic caught the error (Wrong Type):")
    print(e)
    # Output:
    # 1 validation error for AIModelData
    # models
    #   Input should be a valid list [type=list_type, ...]


class AIModelData(BaseModel):
    # Rule: 'name' must have at least 1 character.
    name: str = Field(min_length=1)

    # Rule: 'version' must be greater than 0.
    version: float = Field(gt=0)  # gt = "greater than"

    models: List[str]

    # You can also add rules to optional fields.
    # This field is optional, but if it *is* provided, it must be >= 1
    batch_size: int | None = Field(
        default=None, ge=1
    )  # ge = "greater than or equal to"


# ---
# Failure Case 1: Empty Name
bad_name_data = {
    "name": "",  # This is a string, but its length is 0
    "version": 1.2,
    "models": ["gpt-4"],
}

try:
    AIModelData(**bad_name_data)
except ValidationError as e:
    print("❌ Pydantic caught the empty name:")
    print(e)
    # Output:
    # 1 validation error for AIModelData
    # name
    #   String should have at least 1 character [type=string_too_short, ...]
# ---
# Failure Case 2: Negative Version
bad_version_data = {
    "name": "QueryBot",
    "version": -2.5,  # This is a float, but it's not greater than 0
    "models": ["gpt-4"],
}

try:
    AIModelData(**bad_version_data)
except ValidationError as e:
    print("\n❌ Pydantic caught the bad version:")
    print(e)
    # Output:
    # 1 validation error for AIModelData
    # version
    #   Input should be greater than 0 [type=greater_than, ...]


# BLUEPRINT 1: For the objects INSIDE the list
class ModelDetail(BaseModel):
    name: str = Field(min_length=1)
    type: str  # We'll make 'type' required


# BLUEPRINT 2: The main object
class AIModelData(BaseModel):
    name: str = Field(min_length=1)
    version: float = Field(gt=0)

    # This is the magic part!
    # Pydantic now knows 'models' is a list, and
    # every item IN that list must follow the 'ModelDetail' blueprint.
    models: List[ModelDetail]


# ---
# The Good Data (with all details)
good_complex_data = {
    "name": "QueryBot 5000",
    "version": 1.2,
    "models": [{"name": "gpt-4", "type": "llm"}, {"name": "clip", "type": "vision"}],
}

try:
    # Pydantic validates the outer object AND every inner object.
    data_obj = AIModelData(**good_complex_data)

    print("✅ Pydantic validated the nested data!")

    # You can access it like a normal object
    print(f"First model name: {data_obj.models[0].name}")
    print(f"First model type: {data_obj.models[0].type}")

except ValidationError as e:
    print(f"❌ This shouldn't have failed: {e}")

# ---
# The Bad Data (with the missing 'type' key)
bad_complex_data = {
    "name": "QueryBot 5000",
    "version": 1.2,
    "models": [
        {"name": "gpt-4", "type": "llm"},
        {"name": "dall-e"},  # This one is missing 'type'
    ],
}

try:
    AIModelData(**bad_complex_data)
except ValidationError as e:
    print("\n❌ Pydantic caught the NESTED error:")
    # The error message is incredibly specific:
    print(e)
    # Output:
    # 1 validation error for AIModelData
    # models.1.type  <-- This means: in the 'models' list, at index 1,
    #                     the 'type' field is wrong.
    #   Field required [type=missing, ...]


# Blueprint 1: Inner model
class ModelDetail(BaseModel):
    name: str = Field(min_length=1)
    type: str


# Blueprint 2: Outer model
class AIModelData(BaseModel):
    name: str = Field(min_length=1)
    version: float = Field(gt=0)
    models: List[ModelDetail]


# Our clean, validated Python object
good_data = {
    "name": "QueryBot 5000",
    "version": 1.2,
    "models": [{"name": "gpt-4", "type": "llm"}, {"name": "clip", "type": "vision"}],
}

data_obj = AIModelData(**good_data)

# 'data_obj' is now a Pydantic class object.
# We can't send 'data_obj' in an API response.
# We need to convert it back to a dict or JSON.
# --- EXPORTING ---

# 1. Export to a Python Dictionary
python_dict = data_obj.model_dump()

print("--- As Dictionary ---")
print(python_dict)
print(f"Type is: {type(python_dict)}")
# 2. Export to a JSON String
json_string = data_obj.model_dump_json()

print("\n--- As JSON String ---")
print(json_string)
print(f"Type is: {type(json_string)}")

# ---
# Pro-tip: You can even make it "pretty" for logging
pretty_json = data_obj.model_dump_json(indent=2)
print("\n--- As Pretty JSON ---")
print(pretty_json)
