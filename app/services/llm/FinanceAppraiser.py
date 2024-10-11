from .BaseLLMService import BaseLLMService
from config.llm import llm_response_schema

import json
from jsonschema import validate


class FinanceAppraiser(BaseLLMService):
    def validate_response(self, res) -> None | dict:
        """
        Ensure the response from the LLM is a valid JSON and has the appropriate shape
        Return the parsed version of the JSON if valid and None if not
        """
        try:
            data = json.loads(res)
            validate(instance=data, schema=llm_response_schema)
        except:
            return None
        return data

    # def appraise(
    #     self, symbol, name, industry, metric_info, metric_histories, forecast
    # ) -> dict[str, str]:
    #     # Get a dictionary of local variables
    #     local_vars = locals()
    #     # Remove 'self' from the dictionary
    #     local_vars.pop("self")
    #     # Format the base_prompt with the remaining local variables
    #     prompt = base_prompt.format(**local_vars)

    #     return self.invoke(prompt)
