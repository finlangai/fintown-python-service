from pydantic import BaseModel
from typing import Dict, Any


# THIS FUNCTION IS USED TO MAP CORRESPONSINDG JSON DATA INTO APPROPRIATE SHAPE
def model_mapper(
    model: BaseModel, data: Dict[str, Any], shifted_fields: Dict[str, Any] = {}
):
    fields = model.model_fields
    result = shifted_fields

    for field in fields:
        if field in data:
            result[field] = data.pop(field)
            continue

        field_type = model.__annotations__[field]
        if not issubclass(field_type, BaseModel):
            continue
        # Recursively map embedded models
        result[field] = model_mapper(field_type, data)

    return result
