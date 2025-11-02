# 05_output_export: Converting Clean Data to JSON/Dict

After data is validated, you must convert the Pydantic object back into a standard format for external use (e.g., API responses, database entry).

| Method | Output Format | Primary Use Case |
| :--- | :--- | :--- |
| **`.model_dump()`** | Python `dict` | Passing data to database drivers or internal Python functions. |
| **`.model_dump_json()`**| JSON `str` | Returning the final data from a web API (essential for frameworks like FastAPI/Flask). |

Run `python 05_data_export.py` to see how the validated object is safely converted back.