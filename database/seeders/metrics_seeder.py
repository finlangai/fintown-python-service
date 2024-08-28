import pandas as pd

from app.utils import print_green_bold
from app.services import FormularResolver
from app.models import FormulaRepository, CompanyRepository
from app.enums import FormulaType


def main():
    print("Metrics seeder")
    FormulaRepo = FormulaRepository()
    metric_formulars = list(
        FormulaRepo.find_by(query={"category": FormulaType.FINANCIAL_METRIC})
    )

    CompanyRepo = CompanyRepository()
    # companies = list(CompanyRepo.find_by(query={"_id": "vnm"}))
    companies = list(CompanyRepo.find_by(query={}))

    resolver = FormularResolver(dropna=True)
    for c in companies:
        resolver.update_symbol(c.id)
        print(f"{c.id.upper()}===========================")
        metric_df = pd.DataFrame()
        for metric in metric_formulars:
            metric_df = pd.concat([metric_df, resolver.appraise(metric)], axis=1)

        metric_df = pd.concat([metric_df, resolver.get_meta_df()], axis=1)
        print(metric_df)


if __name__ == "__main__" or __name__ == "tasks":
    main()
