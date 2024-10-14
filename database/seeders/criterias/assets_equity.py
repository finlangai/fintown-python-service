from app.models.Criteria import Criteria, CriteriaCluster

group_of_clusters: list[CriteriaCluster] = []

group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ lệ tăng trưởng tài sản",
        metrics=[
            "assets_growth_rate",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ lệ tăng trưởng vốn chủ sở hữu",
        metrics=[
            "equity_growth_rate",
        ],
    )
)
group_of_clusters.append(
    CriteriaCluster(
        name="Tỷ lệ tăng trưởng lợi nhuận trên tổng tài sản",
        metrics=[
            "return_of_assets_growth_rate",
        ],
    )
)


def get(index: int):
    return Criteria(
        id=index,
        name="Tài sản và Vốn chủ sở hữu",
        slug="assets_equity",
        group=group_of_clusters,
    )
