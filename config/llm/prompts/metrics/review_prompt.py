from langchain.prompts import PromptTemplate

# placeholders: metrics_data, metric_cluster_name, symbol
template = """
system:
Bạn là một chuyên gia phân tích tài chính và đưa ra các nhận định sâu sắc dựa trên dữ liệu quá khứ và dự đoán.

human:
Hãy đọc qua dữ liệu của các chỉ số sau:
{metrics_data}

Yêu cầu: Phân tích ngắn gọn (dưới 150 từ) về {metric_cluster_name} của công ty {symbol} dựa trên dữ liệu đã cho theo tiếng Việt. Tránh đưa ra ý kiến chủ quan, không cần giải thích nguyên nhân, chỉ tập trung vào số liệu, không cần mở đầu bằng dựa trên.
"""
# placeholders: metric_name, metric_name_vi, historical_data, forecasted_data
metric_input_template = """
Chỉ số {metric_name} hay {metric_name_vi}
- Dữ liệu lịch sử:
{historical_data}
- Dữ liệu dự đoán 5 năm
{forecasted_data}
"""
# Create the PromptTemplate
cluster_review_prompt = PromptTemplate(
    template=template,
    variable_map={
        "metrics_data": "metrics_data",
        "metric_cluster_name": "metric_cluster_name",
        "symbol": "symbol",
    },
)
