import re
from unidecode import unidecode


"""Biến một chuỗi ngôn ngữ tự nhiên thành ký tự 
latin dạng chữ thường và snake case"""


def natural_to_snake(text: str):
    # Turn text to lower case
    text = text.lower()

    # Remove roman numeral prefixes, number prefixes, and single uppercase letter prefixes
    text = re.sub(r"^([ivxlcdm]+\.|\d+\.[ \t]*|[a-zA-Z]\.\s*)", "", text)

    # Convert to snake_case
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\w\s]", "", text)

    # Remove any leading underscores
    text = text.lstrip("_")

    # Remove sequence of numbers at the end
    text = re.sub(r"_\d+$", "", text)

    # Ensure no trailing underscores
    text = text.rstrip("_")

    # Convert Vietnamese characters to Latin characters
    text = unidecode(text)

    return text
