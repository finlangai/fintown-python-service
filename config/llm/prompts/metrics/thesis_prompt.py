from langchain.prompts import PromptTemplate

# placeholders: criteria_name, symbol, thesis_input
template = """
system:
Bạn là chuyên gia phân tích tài chính dựa trên các ngữ liệu và tin tức.

human:
Hãy đưa ra nhận định chung về {criteria_name} của công ty {symbol}.
Dựa trên các tiêu chí con đã được nhận định như sau:
{thesis_input}

Lưu ý: Phân tích ngắn gọn (dưới 300 từ) dựa trên dữ liệu đã cho theo tiếng Việt. Tránh đưa ra ý kiến chủ quan, không cần giải thích nguyên nhân, chỉ tập trung vào số liệu, không cần mở đầu bằng dựa trên.
"""

# placeholders: cluster_name, status, review
thesis_input_template = """
- Tiêu chí {cluster_name} được đánh giá {status} với nhận định:
{review}
"""

# Create the PromptTemplate
criteria_thesis_prompt = PromptTemplate(
    template=template,
    variable_map={
        "metric_group": "metric_group",
        "symbol": "symbol",
        "name_indicator": "name_indicator",
        "status": "status",
        "review": "review",
    },
)
