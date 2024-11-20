import pandas as pd
from datetime import datetime


class DividendEdge:
    @staticmethod
    def score_streak(dividend_df: pd.DataFrame):
        # return 0 if no data
        if dividend_df.shape[0] == 0:
            return 0

        # Extract and sort the years
        years = sorted(dividend_df["year"].tolist(), reverse=True)

        current_year = datetime.now().year

        # set a flag to see if it is valid to count
        # Determine the consecutive streak starting from the most recent year
        last_paid_year = max(years)

        is_valid = current_year == last_paid_year or current_year - 1 == last_paid_year

        # if the last paid year was not current year or last year, have it as interrupted
        if not is_valid:
            return 2

        # this count on the previous that the year array has been sorted desc
        current_streak = 1
        for index in range(1, len(years)):
            curr_index_year = years[index]
            previous_index_year = years[index - 1]

            if curr_index_year == previous_index_year - 1:
                current_streak += 1
            else:
                break

        # Determine the points based on the streak
        if current_streak > 10:
            score = 10
        elif current_streak == 10:
            score = 8
        elif current_streak >= 5:
            score = 6
        elif current_streak >= 3:
            score = 4
        else:
            score = 2

        return score

    @staticmethod
    def score_dividend_growth(dividend_df: pd.DataFrame):
        current_year = datetime.now().year

        filtered_df = dividend_df.query(
            f"{current_year - 3} <= year <= {current_year - 1}"
        )
        number_of_rows = filtered_df.shape[0]

        # 0 if no dividend in the last three years
        if number_of_rows == 0:
            return 0
        # 2 if only one record
        if number_of_rows == 1:
            return 2

        filtered_df["growth_rate"] = filtered_df["cash"].pct_change()
        avg_growth = filtered_df["growth_rate"].mean() * 100

        # return 10 if equal to 10% or more
        if avg_growth >= 10:
            return 10

        # return 8 if growth rate between 5% - 10%
        if avg_growth >= 5:
            return 8

        # return 6 if growth rate between 0% - 5%
        if avg_growth > 0:
            return 6

        # return 4 if the growth rate is 0
        if avg_growth == 0:
            return 4

        # return 2 if negative which is the only case left
        return 2
