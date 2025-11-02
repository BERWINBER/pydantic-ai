# 01_basics: The Core Problem and the BaseModel Solution

The most common data validation problem in Python is the unpredictable **KeyError** or **TypeError** when processing a raw dictionary.

**The Pydantic Solution:** The **`BaseModel`** creates a **blueprint** (a class) that forces the incoming dictionary to meet the expected structure. If it fails, Pydantic throws a single, clear `ValidationError` *immediately*, preventing random crashes later.

Run `python 01_data_validation.py` to see the core mechanism in action.