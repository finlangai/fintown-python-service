from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    text_to_blue,
)
from app.models import CompanyRepository, DividendRepository, FormularRepository
from app.services import StockQuoteService
from app.services import (
    FormularResolver,
    TrendingEdge,
    DividendEdge,
    ReturnsEdge,
    RevenueProfitEdge,
    MomentumEdge,
)
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
    formularResolver = FormularResolver(period="quarter", dropna=True)

    required_identifiers = [
        "return_on_equity",
        "return_on_assets",
        "revenue_growth_rate",
        "net_profit_growth_rate",
        "net_profit_margin",
    ]
    formular_dict = FormularRepository().get_dict(required_identifiers)

    # Get the current date
    current_date = datetime.now().date()
    # Format the current date as YYYY-MM-DD
    today = current_date.strftime("%Y-%m-%d")
    # Calculate the date 52 weeks before today
    date_52_weeks_ago = current_date - timedelta(weeks=52)
    # Format the date 52 weeks ago as YYYY-MM-DD
    today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

    # delta in day, delta in week, delta in month, delta in year

    # for symbol in ["HPG"]:
    # for symbol in ["VNM", "BVH", "VCB", "HPG", "MBB", "GAS"]:
    for symbol in symbol_list:
        # update symbol for resolver
        formularResolver.update_symbol(symbol)

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
        print("= TRENDING_SCORE: ", TRENDING_SCORE)

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
        print("= DIVIDEND_SCORE: ", DIVIDEND_SCORE)

        # ==================================
        # ========= RETURNS SCORE =========
        # ==================================
        print("=== RETURNS")
        EPS_SCORE = ReturnsEdge.score_eps(formularResolver)
        ROA_SCORE = ReturnsEdge.score_roa(
            formularResolver, formular_dict["return_on_assets"]
        )
        ROE_SCORE = ReturnsEdge.score_roe(
            formularResolver, formular_dict["return_on_equity"]
        )

        RETURNS_SCORE = EPS_SCORE * 0.4 + ROA_SCORE * 0.3 + ROE_SCORE * 0.3

        print("EPS_SCORE: ", EPS_SCORE)
        print("ROA_SCORE: ", ROA_SCORE)
        print("ROE_SCORE: ", ROE_SCORE)

        print("= RETURNS_SCORE: ", RETURNS_SCORE)

        # ========================================
        # ========= REVENUE PROFIT SCORE =========
        # ========================================
        print("=== REVENUE PROFIT")
        PROFIT_SCORE = RevenueProfitEdge.scrore_profit(
            formularResolver, formular_dict["net_profit_growth_rate"]
        )
        REVENUE_SCORE = RevenueProfitEdge.scrore_revenue(
            formularResolver, formular_dict["revenue_growth_rate"]
        )

        NPM_SCORE = RevenueProfitEdge.scrore_npm(
            formularResolver, formular_dict["net_profit_margin"]
        )

        REVENUE_PROFIT_SCORE = (
            PROFIT_SCORE * 0.4 + REVENUE_SCORE * 0.3 + NPM_SCORE * 0.3
        )

        print("PROFIT_SCORE: ", PROFIT_SCORE)
        print("REVENUE_SCORE: ", REVENUE_SCORE)
        print("NPM_SCORE: ", NPM_SCORE)

        print("= REVENUE_PROFIT_SCORE: ", REVENUE_PROFIT_SCORE)

        # ========================================
        # ========= REVENUE PROFIT SCORE =========
        # ========================================
        print("=== MOMENTUM")

        MOMENTUM_7D_SCORE = MomentumEdge.score_7d(quotes_df)
        MOMENTUM_30D_SCORE = MomentumEdge.score_30d(quotes_df)
        MOMENTUM_90D_SCORE = MomentumEdge.score_90d(quotes_df)
        MOMENTUM_1Y_SCORE = MomentumEdge.score_1Y(quotes_df)

        MOMENTUM_SCORE = (
            MOMENTUM_7D_SCORE * 0.2
            + MOMENTUM_30D_SCORE * 0.25
            + MOMENTUM_90D_SCORE * 0.25
            + MOMENTUM_1Y_SCORE * 0.1
        )

        print("MOMENTUM_7D_SCORE: ", MOMENTUM_7D_SCORE)
        print("MOMENTUM_30D_SCORE: ", MOMENTUM_30D_SCORE)
        print("MOMENTUM_90D_SCORE: ", MOMENTUM_90D_SCORE)
        print("MOMENTUM_1Y_SCORE: ", MOMENTUM_1Y_SCORE)

        print("= MOMENTUM_SCORE: ", MOMENTUM_SCORE)

        # === CALCULATING FINAL DATA
        Q_RATING = (
            TRENDING_SCORE
            + DIVIDEND_SCORE
            + RETURNS_SCORE
            + REVENUE_PROFIT_SCORE
            + MOMENTUM_SCORE
        ) / 5

        # update into stash
        comparison_data = {
            "rating": Q_RATING,
            "trending": TRENDING_SCORE,
            "dividend": DIVIDEND_SCORE,
            "returns": RETURNS_SCORE,
            "revenueProfit": REVENUE_PROFIT_SCORE,
            "momentum": MOMENTUM_SCORE,
        }

        mongodb.update_one("stash", {"symbol": symbol}, {"comparison": comparison_data})
        print(text_to_blue(f"Comparison data for {text_to_red(symbol)} updated"))


if __name__ == "__main__" or __name__ == "tasks":
    main()
