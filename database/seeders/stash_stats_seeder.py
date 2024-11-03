from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    time,
)
from app.models import CompanyRepository, FormularRepository
from app.services import StockQuoteService, FormularResolver
from app.enums import ParamLocation

from core import mongodb
import numpy as np, pandas as pd, json
from datetime import timedelta


def main():
    """
    *Notice: depend on symbols inside companies collection

    This seeder in charge of:
        market cap
        price
        P/E ltm
        P/B ltm
        ROE ltm
        BVPS ltm
        EPS ltm
    """
    print_green_bold("=== SEEDING STATS FOR STASH")
    # get the list of symbol from companies symbol
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    financeService = FormularResolver()
    quoteService = StockQuoteService()

    # get the date range
    today = time.today_str()
    five_days_ago = time.date_from(timedelta(days=5))

    for symbol in symbol_list:
        # =========================================
        # ========= GET LAST CLOSED PRICE =========
        # =========================================
        last_closed_price = float(
            quoteService.history(
                start=five_days_ago, end=today, interval="1D", symbol=symbol
            ).iloc[-1]["close"]
            * 1000
        )

        # =========================================
        # ========== CALCULATE MARKETCAP ==========
        # =========================================
        # calculate marketcap
        financeService.update_symbol(symbol)
        outstanding_share = float(
            financeService.get_data(ParamLocation.ratio).iloc[0][
                "Outstanding Share (Mil. Shares)"
            ]
        )
        marketcap = last_closed_price * outstanding_share

        # =========================================
        # =========== CALCULATE METRICS ===========
        # =========================================
        # get required metric formulars
        identifier_list = [
            "return_on_equity",
            "book_value_per_share",
            "earnings_per_share",
        ]
        formular_list = list(
            FormularRepository().find_by({"identifier": {"$in": identifier_list}})
        )
        metric_df = pd.concat(
            [financeService.appraise(formular) for formular in formular_list], axis=1
        )
        # calculate LTM
        roe_ltm = float(metric_df.head(4)["return_on_equity"].sum() / 4)
        eps_ltm = float(metric_df.head(4)["earnings_per_share"].sum())
        bvps_ltm = float(metric_df.iloc[0]["book_value_per_share"])
        pe_ltm = last_closed_price / eps_ltm
        pb_ltm = last_closed_price / bvps_ltm

        stats_dict = {
            "last_closed_price": last_closed_price,
            "marketcap": marketcap,
            "outstanding_share": outstanding_share,
            "pe_ltm": pe_ltm,
            "pb_ltm": pb_ltm,
            "roe_ltm": roe_ltm,
            "eps_ltm": eps_ltm,
            "bvps_ltm": bvps_ltm,
        }
        mongodb.update_one("stash", {"symbol": symbol}, {"stats": stats_dict})
        print_green_bold(f"stats updated for {symbol}")

    # run fluctuation seeder also
    from database.seeders import deltas_seeder, fluctuation_seeder

    deltas_seeder.main()
    fluctuation_seeder.main()

    # return the count of symbol
    return len(symbol_list)


if __name__ == "__main__" or __name__ == "tasks":
    main()
