from app.models.Criteria import Criteria, CriteriaCluster

group_of_clusters: list[CriteriaCluster] = []
group_of_clusters.append(
    CriteriaCluster(
        name="Hiệu quả sinh lời dựa trên vốn",
        metrics=[
            "return_on_equity",
            "return_on_assets",
            "return_on_capital_employed",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Biên lợi nhuận",
        metrics=["gross_profit_margin", "net_profit_margin"],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ suất lợi nhuận trên doanh thu",
        metrics=["return_on_sales"],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Lợi nhuận trên mỗi cổ phần",
        metrics=["earnings_per_share"],
    )
)


def get(index: int):
    return Criteria(
        id=index,
        name="Hiệu quả sinh lời",
        slug="profitability",
        group=group_of_clusters,
    )
