from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models.Company import CompanyMovingAverage, CompanyRepository
from app.services import StockQuoteService

from core import mongodb
import numpy as np
from datetime import datetime, timedelta


def main():
    print_green_bold("=== FINDING BEST COMPANY BY NET PROFIT MARGIN")


if __name__ == "__main__" or __name__ == "tasks":
    main()
