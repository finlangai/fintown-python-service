from langchain.prompts import PromptTemplate

template = """
system:
Bạn là chuyên gia phân tích tài chính dựa trên tin tức: {assessment}.

human:
Yêu cầu phân loại tin tức vào một trong các loại sau: Tiêu cực, Tích cực.
Chỉ trả lời 1 trong 2 lựa chọn trên và không cần gì thêm.
"""

# Create the PromptTemplate
status_prompt = PromptTemplate(
    template=template, variable_map={"assessment": "assessment"}
)
