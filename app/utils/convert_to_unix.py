import re


# Function to extract and convert the timestamp
def convert_to_unix_timestamp(date_str):
    if date_str is None:
        return None
    match = re.search(r"\d+", date_str)
    if match:
        return int(match.group(0))
    return None
