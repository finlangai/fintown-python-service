from langchain.prompts import PromptTemplate

# placeholders: symbol, industry, revenue_df, net_profit_df, npm_df
template = """
system:
Bạn là chuyên gia phân tích tài chính dựa trên các số liệu từ báo cáo tài chính và chỉ số tài chính.

human:
Hãy đưa ra nhận định ngắn dưới 39 từ về doanh thu, lợi nhuận ròng và biên lợi nhuận ròng của công ty {symbol} thuộc ngành {industry} đến năm mới nhất.
Dưới đây là thông tin của các số liệu dưới dạng Dataframe:
- Doanh thu
{revenue_df}

- Lợi nhuận ròng
{net_profit_df}

- Biên lợi nhuận ròng
{npm_df}

Lưu ý:
- sử dụng đơn vị tỷ đồng cho doanh thu và lợi nhuận nếu nhắc đến, sử dụng % nếu là biên lợi nhuận ròng
- phân tích và trả lời ngắn gọn dựa trên dữ liệu đã cho theo tiếng Việt.
- không xuống dòng
- không cần mở đầu bằng dựa trên
- Không cần lặp lại nội dung câu hỏi
"""

# Create the PromptTemplate
best_symbol_comment_prompt = PromptTemplate(
    template=template,
    variable_map={
        "symbol": "symbol",
        "industry": "industry",
        "revenue_df": "revenue_df",
        "net_profit_df": "net_profit_df",
        "npm_df": "npm_df",
    },
)
