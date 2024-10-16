from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models import MetricHistoryRepository
from app.services import StockQuoteService, BaseLLMService

from config.llm.prompts import best_symbol_comment_prompt
from core import mongodb
import numpy as np, pandas as pd
from datetime import datetime, timedelta


def main():
    print_green_bold("=== FINDING BEST COMPANY BY NET PROFIT MARGIN")

    metricRepo = MetricHistoryRepository()
    llm = BaseLLMService()

    metrics = metricRepo.get_collection().aggregate(
        pipeline=[
            {"$sort": {"year": -1, "quarter": -1}},
            {"$group": {"_id": "$symbol", "latest_record": {"$first": "$$ROOT"}}},
            {"$replaceRoot": {"newRoot": "$latest_record"}},
        ]
    )
    metrics = list(metrics)
    npm_list = [
        {
            "symbol": record["symbol"],
            "Net Profit Margin": record["metrics"]["net_profit_margin"],
        }
        for record in metrics
    ]
    npm_df = pd.DataFrame(npm_list)

    best_symbol = npm_df.loc[npm_df["Net Profit Margin"].idxmax()]["symbol"]

    # ==================================================================
    # ====== remove flag and assessment from previous best symbol ======
    # ==================================================================
    mongodb.get_collection("stash").update_one(
        {"is_best_by_npm": True}, {"$unset": {"is_best_by_npm": "", "insight": ""}}
    )

    # =================================================================
    # ====================== GENERATE ASSESSMENT ======================
    # =================================================================
    stash = mongodb.find_one("stash", {"symbol": best_symbol})

    revenue_historical = [
        {"year": record["year"], "revenue": record["revenue"]}
        for record in stash["year"]
    ]
    net_profit_historical = [
        {"year": record["year"], "net_profit": record["net_profit"]}
        for record in stash["year"]
    ]

    npm_historical = metricRepo.get_collection().find(
        filter={"symbol": best_symbol, "quarter": 0},
        sort={"year": -1},
        limit=5,
        projection={
            "_id": 0,
            "year": 1,
            "net_profit_margin": "$metrics.net_profit_margin",
        },
    )
    npm_historical = list(npm_historical)

    # create 3 required dataframe
    revenue_df = pd.DataFrame(revenue_historical)
    net_profit_df = pd.DataFrame(net_profit_historical)
    npm_df = pd.DataFrame(npm_historical)

    #  get the industry of the company
    industry = mongodb.get_collection("companies").find_one(
        filter={"symbol": best_symbol}, projection={"industry": 1}
    )["industry"]

    prompt = best_symbol_comment_prompt.format(
        symbol=best_symbol,
        industry=industry,
        revenue_df=revenue_df.to_string(),
        net_profit_df=net_profit_df.to_string(),
        npm_df=npm_df.to_string(),
    )
    assessment = llm.invoke(prompt)

    # ===================================================================
    # ================ UPDATE STASH FOR THE BEST SYMBOL  ================
    # ===================================================================
    # update flag and assessment for the best symbol
    mongodb.update_one(
        "stash",
        {"symbol": best_symbol},
        {"is_best_by_npm": True, "assessment": assessment},
    )
    print_green_bold(f"Updated! The best symbol by Net Profit Margin is {best_symbol}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
