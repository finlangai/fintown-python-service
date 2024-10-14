from app.models.Criteria import Criteria, CriteriaCluster

group_of_clusters: list[CriteriaCluster] = []
group_of_clusters.append(
    CriteriaCluster(
        name="Khả năng thanh khoản",
        metrics=[
            "current_ratio",
            "quick_ratio",
            "cash_ratio",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ số thanh toán lãi vay",
        metrics=[
            "interest_coverage_ratio",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ số nợ trên tài sản",
        metrics=[
            "debt_to_assets_ratio",
        ],
    )
)


def get(index: int):
    return Criteria(
        id=index,
        name="Khả năng thanh toán",
        slug="solvency",
        group=group_of_clusters,
    )
