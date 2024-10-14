from app.models.Criteria import Criteria, CriteriaCluster

group_of_clusters: list[CriteriaCluster] = []
group_of_clusters.append(
    CriteriaCluster(
        name="Tăng trưởng dòng tiền tự do",
        metrics=["free_cash_flow", "free_cash_flow_growth_rate"],
    )
)


def get(index: int):
    return Criteria(
        id=index,
        name="Dòng tiền",
        slug="cashflow",
        group=group_of_clusters,
    )
