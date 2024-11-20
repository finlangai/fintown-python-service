from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models import CompanyRepository, DividendRepository, FormularRepository
from app.services import StockQuoteService
from app.services.comparison import TrendingEdge, DividendEdge
from app.enums import DividendType

from core import mongodb
import numpy as np, pandas as pd, json
from datetime import datetime, timedelta


def main():
    print_green_bold("=== SEEDING COMPARISON DATA")
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    quoteService = StockQuoteService()
    dividendRepo = DividendRepository()

    required_identifiers = [
        "earnings_per_share",
        "return_of_equity",
        "return_of_assets",
    ]
    required_formulars = (
        FormularRepository()
        .get_collection()
        .find({"identifier": {"$in": required_identifiers}})
    )
    print(required_formulars)

    # Get the current date
    current_date = datetime.now().date()
    # Format the current date as YYYY-MM-DD
    today = current_date.strftime("%Y-%m-%d")
    # Calculate the date 52 weeks before today
    date_52_weeks_ago = current_date - timedelta(weeks=52)
    # Format the date 52 weeks ago as YYYY-MM-DD
    today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

    # delta in day, delta in week, delta in month, delta in year

    for symbol in ["VNM", "BVH", "VCB", "HPG"]:
        print(f"====== {text_to_red(symbol)}")
        quotes_df = quoteService.history(
            symbol=symbol, start=today_52w_before, end=today, interval="1D"
        )

        # ==================================
        # ========= TRENDING SCORE =========
        # ==================================
        print("=== TRENDING")
        is_MA200_growing = TrendingEdge.is_MA200_growing(quotes_df)
        is_MA50_gt_MA100 = TrendingEdge.is_MA50_gt_MA100(quotes_df)
        is_MA100_gt_MA150 = TrendingEdge.is_MA100_gt_MA150(quotes_df)
        is_MA150_gt_MA200 = TrendingEdge.is_MA150_gt_MA200(quotes_df)

        MA_SCORE = TrendingEdge.score_ma(
            is_MA200_growing, is_MA50_gt_MA100, is_MA100_gt_MA150, is_MA150_gt_MA200
        )
        PRICE_SCORE = TrendingEdge.score_stock_price(quotes_df)
        VOLUME_SCORE = TrendingEdge.score_volume(quotes_df)

        # SCORING THE WHOLE EDGE
        TRENDING_SCORE = MA_SCORE * 0.6 + PRICE_SCORE * 0.3 + VOLUME_SCORE * 0.1

        print("MA_SCORE: ", MA_SCORE)
        print("PRICE_SCORE: ", PRICE_SCORE)
        print("VOLUME_SCORE: ", VOLUME_SCORE)

        print("Điểm khía cạnh: ", TRENDING_SCORE)

        # ==================================
        # ========= DIVIDEND SCORE =========
        # ==================================
        print("=== DIVIDEND")
        raw_dividends = [
            record.model_dump() for record in dividendRepo.get_by_symbol(symbol)
        ]
        dividend_df = pd.json_normalize(raw_dividends)
        # only keep cash dividend records
        dividend_df = dividend_df[dividend_df["type"] == DividendType.CASH]
        dividend_df = (
            dividend_df.groupby("year")["cash"]
            .sum()
            .reset_index()
            .sort_values(by="year", ascending=True)
        )
        ANNUAL_PAYMENT_SCORE = DividendEdge.score_streak(dividend_df)

        DIVIDEND_GROWTH_SCORE = DividendEdge.score_dividend_growth(dividend_df)

        DIVIDEND_SCORE = ANNUAL_PAYMENT_SCORE * 0.6 + DIVIDEND_GROWTH_SCORE * 0.4

        print("ANNUAL_PAYMENT_SCORE: ", ANNUAL_PAYMENT_SCORE)
        print("DIVIDEND_GROWTH_SCORE: ", DIVIDEND_GROWTH_SCORE)
        print("Điểm khía cạnh: ", DIVIDEND_SCORE)

        # ==================================
        # ========= RETURNS SCORE =========
        # ==================================
        print("=== RETURNS")
        # raw_dividends = [
        #     record.model_dump() for record in dividendRepo.get_by_symbol(symbol)
        # ]
        # dividend_df = pd.json_normalize(raw_dividends)
        # # only keep cash dividend records
        # dividend_df = dividend_df[dividend_df["type"] == DividendType.CASH]
        # dividend_df = (
        #     dividend_df.groupby("year")["cash"]
        #     .sum()
        #     .reset_index()
        #     .sort_values(by="year", ascending=True)
        # )
        # ANNUAL_PAYMENT_SCORE = DividendEdge.score_streak(dividend_df)

        # DIVIDEND_GROWTH_SCORE = DividendEdge.score_dividend_growth(dividend_df)

        # DIVIDEND_SCORE = ANNUAL_PAYMENT_SCORE * 0.6 + DIVIDEND_GROWTH_SCORE * 0.4

        # print("ANNUAL_PAYMENT_SCORE: ", ANNUAL_PAYMENT_SCORE)
        # print("DIVIDEND_GROWTH_SCORE: ", DIVIDEND_GROWTH_SCORE)
        # print("Điểm khía cạnh: ", DIVIDEND_SCORE)

        # mongodb.update_one("stash", {"symbol": symbol}, {"comparison": delta_dict})


if __name__ == "__main__" or __name__ == "tasks":
    main()
