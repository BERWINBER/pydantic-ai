# 02_constraints: Adding Guardrails with `Field`

Type hints only check the *type* (`int`, `str`). But for AI/ML tasks, you need to check the *value* against specific **constraints**.

The **`Field`** function allows you to add specific constraints on the value of a field, turning your blueprint into a powerful data quality gate. For example, a probability must be between 0 and 1.

| Constraint | Meaning | Example Use |
| :--- | :--- | :--- |
| `ge` / `le` | Greater/Less than or Equal to | Enforcing a probability score is $\le 1.0$. |
| `min_length` | Minimum string length | Ensuring a prompt or file name is not empty. |

Run `python 02_field_constraints.py` to see how Pydantic enforces numeric and string constraints.