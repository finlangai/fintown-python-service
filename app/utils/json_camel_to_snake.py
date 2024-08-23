import inflection


# THIS FUNCTION IS USED WITH OBJECT
def json_camel_to_snake(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = inflection.underscore(key)
            new_data[new_key] = json_camel_to_snake(value)
        return new_data
    elif isinstance(data, list):
        return [json_camel_to_snake(item) for item in data]
    else:
        return data
