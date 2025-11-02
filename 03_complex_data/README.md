# 03_complex_data: Models Inside Models (Handling Hierarchical Data)

AI outputs and complex APIs rarely return flat data. To validate structures like a list of extracted entities, you need **nested models**.

**How it Works:**
1.  Define a **small, inner `BaseModel`** for the repeating object (e.g., `ExtractedPerson`).
2.  Use that model as a type hint in the **outer `BaseModel`** (e.g., `List[ExtractedPerson]`).

Pydantic automatically drills down and validates every item in the list, providing a precise error location if a nested object is invalid.

Run `python 03_nested_models.py` to see how Pydantic pinpoints an error inside a nested list.