from langchain.prompts import PromptTemplate

# placeholders: symbol, overall_input
template = """
system:
Bạn là chuyên gia phân tích tài chính dựa trên các ngữ liệu và tin tức.

human:
Hãy đưa ra nhận định chung về chất lượng tăng trưởng của công ty {symbol}.
Dựa trên các tiêu chí con đã được nhận định như sau:
{overall_input}

Lưu ý: Kết thúc mỗi ý bằng dấu ';', phân tích ngắn gọn (dưới 300 từ) dựa trên dữ liệu đã cho theo tiếng Việt. Tránh đưa ra ý kiến chủ quan, không cần giải thích nguyên nhân, chỉ tập trung vào số liệu, không cần mở đầu bằng dựa trên.
"""
# placeholders: criteria_name, status, assessment
overall_input_template = """
- Tiêu chí {criteria_name} được đánh giá {status} với nhận định:
{assessment}
"""

# Create the PromptTemplate
overall_prompt = PromptTemplate(
    template=template,
    variable_map={
        "symbol": "symbol",
        "criteria_name": "criteria_name",
        "status": "status",
        "assessment": "assessment",
    },
)
