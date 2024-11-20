import pandas as pd


class TrendingEdge:
    @staticmethod
    def score_ma(value1, value2, value3, value4):
        # Điểm gốc
        base_score = 2

        # Cộng thêm 2 điểm cho mỗi giá trị True
        additional_score = sum([value1, value2, value3, value4]) * 2

        # Tổng điểm
        total_score = base_score + additional_score

        return total_score

    @staticmethod
    def score_stock_price(quotes_df: pd.DataFrame):
        base_score = 0

        # score 0 if has no data
        if quotes_df.shape[0] < 50:
            return base_score

        # plus 2 if have data
        base_score += 2

        close_series = quotes_df["close"]

        highest_price = close_series.max()
        lowest_price = close_series.min()
        current_price = close_series.iloc[-1]

        is_gt_MA50 = current_price > TrendingEdge.get_latest_MA50(quotes_df)
        is_within_25_percent = current_price >= 0.75 * highest_price
        is_30_percent_gt_lowest = current_price > lowest_price * 1.3

        # add score
        base_score += (
            sum([is_gt_MA50, is_within_25_percent, is_30_percent_gt_lowest]) * 2
        )

        return base_score

    @staticmethod
    def score_volume(quotes_df: pd.DataFrame):
        avg_volume = quotes_df["volume"].tail(10).mean()

        if avg_volume > 1000000:
            return 10
        elif avg_volume > 700000:
            return 8
        elif avg_volume > 400000:
            return 6
        elif avg_volume > 100000:
            return 4
        else:
            return 2

        return avg_volume

    @staticmethod
    def is_MA200_growing(quotes_df: pd.DataFrame) -> bool:
        if quotes_df.shape[0] < 230:
            return False
        quotes_df["MA200"] = quotes_df["close"].rolling(window=200).mean()
        ma_200_now = float(quotes_df["MA200"].iloc[-1])
        ma_200_30d_ago = float(quotes_df["MA200"].iloc[-30])
        return ma_200_now > ma_200_30d_ago

    @staticmethod
    def is_MA50_gt_MA100(quotes_df: pd.DataFrame) -> bool:
        if quotes_df.shape[0] < 100:
            return False

        ma_50_now = TrendingEdge.get_latest_MA50(quotes_df)
        ma_100_now = TrendingEdge.get_latest_MA100(quotes_df)

        return ma_50_now > ma_100_now

    @staticmethod
    def is_MA100_gt_MA150(quotes_df: pd.DataFrame) -> bool:
        if quotes_df.shape[0] < 150:
            return False

        ma_100_now = TrendingEdge.get_latest_MA100(quotes_df)
        ma_150_now = TrendingEdge.get_latest_MA150(quotes_df)

        return ma_100_now > ma_150_now

    @staticmethod
    def is_MA150_gt_MA200(quotes_df: pd.DataFrame) -> bool:
        if quotes_df.shape[0] < 200:
            return False

        ma_150_now = TrendingEdge.get_latest_MA150(quotes_df)
        ma_200_now = TrendingEdge.get_latest_MA200(quotes_df)

        return ma_150_now > ma_200_now

    @staticmethod
    def get_latest_MA50(quotes_df: pd.DataFrame):
        quotes_df["MA50"] = quotes_df["close"].rolling(window=50).mean()
        ma_50_now = float(quotes_df["MA50"].iloc[-1])
        return ma_50_now

    @staticmethod
    def get_latest_MA100(quotes_df: pd.DataFrame):
        quotes_df["MA100"] = quotes_df["close"].rolling(window=100).mean()
        ma_100_now = float(quotes_df["MA100"].iloc[-1])
        return ma_100_now

    @staticmethod
    def get_latest_MA150(quotes_df: pd.DataFrame):
        quotes_df["MA150"] = quotes_df["close"].rolling(window=150).mean()
        ma_150_now = float(quotes_df["MA150"].iloc[-1])
        return ma_150_now

    @staticmethod
    def get_latest_MA200(quotes_df: pd.DataFrame):
        quotes_df["MA200"] = quotes_df["close"].rolling(window=200).mean()
        ma_200_now = float(quotes_df["MA200"].iloc[-1])
        return ma_200_now
