from .BaseLLMService import BaseLLMService
from config.llm import base_prompt


class FinanceAppraiser(BaseLLMService):
    def prompting(
        self, symbol, name, industry, metric_info, metric_histories, forecast
    ):
        # Get a dictionary of local variables
        local_vars = locals()
        # Remove 'self' from the dictionary
        local_vars.pop("self")
        # Format the base_prompt with the remaining local variables
        prompt = base_prompt.format(**local_vars)

        return self.invoke(prompt)
