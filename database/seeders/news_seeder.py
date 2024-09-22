from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import StockInfoService
from app.models import News, NewsRepository
from config.seeder import STOCK_SYMBOLS


def main():
    print_green_bold("=== SEEDING EVENTS")

    infoService = StockInfoService()
    newsRepo = NewsRepository()

    for symbol in STOCK_SYMBOLS:
        # update symbol
        infoService.update_symbol(symbol)

        # get events dataframe of the company
        news_df = infoService.news()

        # add symbol column
        news_df.insert(0, "symbol", symbol)

        # loop through each row in the dataframe and accumulate News model into events variable
        news: list[News] = []
        for _, row in news_df.iterrows():
            dict = row.to_dict()
            news.append(News(**dict))

        # insert db
        newsRepo.save_many(news)

        print(f"{len(news)} news inserted for {text_to_red(symbol)}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
