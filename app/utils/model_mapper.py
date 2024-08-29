from pydantic import BaseModel
from typing import Dict, Any
import inspect


def model_mapper(
    model: BaseModel, data: Dict[str, Any], shifted_fields: Dict[str, Any] = {}
):
    """
    THIS FUNCTION IS USED TO MAP CORRESPONSINDG JSON DATA INTO APPROPRIATE SHAPE
    """
    fields = model.model_fields
    result: dict = shifted_fields

    for field in fields:
        if field in data:
            result[field] = data.pop(field)
            continue
        field_type = model.__annotations__[field]
        if not isinstance(field_type, type):
            continue
        if not issubclass(field_type, BaseModel):
            continue
        # Recursively map embedded models
        result[field] = model_mapper(field_type, data)

    return result
