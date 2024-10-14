from app.models.Criteria import Criteria, CriteriaCluster

group_of_clusters: list[CriteriaCluster] = []
group_of_clusters.append(
    CriteriaCluster(
        name="Tăng trưởng doanh thu",
        metrics=[
            "revenue_growth_rate",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tăng trưởng lợi nhuận",
        metrics=[
            "gross_profit_growth_rate",
            "net_profit_growth_rate",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tăng trưởng lợi nhuận trước lãi vay, thuế và khấu hao",
        metrics=[
            "ebitda",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tăng trưởng lợi nhuận trên mỗi cổ phần",
        metrics=[
            "earnings_per_share_growth_rate",
        ],
    )
)


def get(index: int):
    return Criteria(
        id=index,
        name="Doanh thu và Lợi nhuận",
        slug="revenue_profit",
        group=group_of_clusters,
    )
