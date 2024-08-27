from app.services.formular_eval import ResolverToolkit
from app.models import Formular


class FormularResolver(ResolverToolkit):
    def appraise(self, metric: Formular):
        for formular in metric.library:
            is_sufficient = self.check_sufficiency(parameters=formular.parameters)
            # if not is_sufficient:
            #     continue
            # print(formular.name)
            evaluating = formular.expression

            print(f"{is_sufficient} for {formular.name} with {self.symbol}")
            for param in formular.parameters:
                pass
