from pydantic import BaseModel
from typing import Dict, Any
from copy import copy


def model_mapper(
    model: BaseModel, data: Dict[str, Any], shifted_fields: Dict[str, Any] = {}
) -> dict:
    """
    THIS FUNCTION IS USED TO MAP CORRESPONSINDG JSON DATA INTO APPROPRIATE SHAPE

    model: the pydantic model with required fields
    data: the dict that contains raw and unmapped data
    shifted_fields: for manually adding additional fields to the result
    """
    fields = model.model_fields
    result: dict = copy(shifted_fields)

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
        result[field] = model_mapper(model=field_type, data=data)

    return result
