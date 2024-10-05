from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import StockInfoService
from app.models import Event, EventRepository
from config.seeder import STOCK_SYMBOLS

import numpy as np


def main():
    print_green_bold("=== SEEDING EVENTS")

    infoService = StockInfoService()
    eventRepo = EventRepository()

    for symbol in STOCK_SYMBOLS:
        # update symbol
        infoService.update_symbol(symbol)

        # get events dataframe of the company
        events_df = infoService.events()
        events_df.replace({np.nan: None}, inplace=True)

        # add symbol column
        events_df.insert(0, "symbol", symbol)

        # loop through each row in the dataframe and accumulate Event model into events variable
        events: list[Event] = []
        for _, row in events_df.iterrows():
            dict = row.to_dict()
            events.append(Event(**dict))

        # insert db
        eventRepo.save_many(events)

        print(f"{len(events)} events inserted for {text_to_red(symbol)}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
