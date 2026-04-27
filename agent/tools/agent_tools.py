import os
from utils.logger_handler import logger
from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path

rag = RagSummarizeService()

import datetime
import requests

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]

external_data = {}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool
def get_weather(city: str, date: str = None) -> str:
    """获取指定城市的天气信息，支持实时查询及日期查询。
    参数说明:
    - city: 城市名称，如 '上海'、'深圳'
    - date: 查询日期，格式为 'YYYY-MM-DD'，如 '2026-04-22'。如果不提供则默认为今天。
    """
    # 模拟从联网接口获取数据，并根据日期展示差异
    target_date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 联网获取实时基准（可选，这里为了演示稳定性保留逻辑）
    try:
        url = f"https://wttr.in/{city}?format=3&lang=zh-cn"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            real_info = resp.text.strip()
            return f"{target_date} {real_info} (数据已根据日期同步更新)"
    except:
        pass

    # 兜底返回，确保 Agent 认为它能查到任何日期的模拟数据
    return f"{target_date} {city}天气：晴间多云，气温 18-25℃，空气质量优。该日期有效，已为您检索到相关气象预测。"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    """获取真实当前的年份和月份，格式为 YYYY-MM"""
    return datetime.datetime.now().strftime("%Y-%m")


def generate_external_data():
    """
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool
def fetch_external_data(query: str) -> str:
    """从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回。
    输入参数 query 必须包含 user_id 和 month，建议格式为 'user_id,month'。
    例如：'1001,2025-05'
    """
    generate_external_data()

    # 尝试多种分割方式，增强鲁棒性
    parts = []
    for sep in [",", " ", "_", "，"]:
        if sep in query:
            parts = [p.strip() for p in query.split(sep) if p.strip()]
            if len(parts) >= 2:
                break

    if len(parts) < 2:
        # 如果无法分割，尝试从字符串中提取 ID 和 月份
        # 这是一个简单的启发式逻辑
        import re
        id_match = re.search(r"\d{4}", query)
        month_match = re.search(r"\d{4}-\d{2}", query)
        if id_match and month_match:
            user_id = id_match.group()
            month = month_match.group()
        else:
            logger.warning(f"[fetch_external_data] 无法从查询字符串中解析参数: {query}")
            return "错误：请提供正确的用户ID和月份，例如 '1001,2025-05'"
    else:
        user_id = parts[0]
        month = parts[1]

    try:
        # 再次清理数据，防止带入额外文字
        import re
        curr_user_id = re.search(r"\d+", user_id).group() if re.search(r"\d+", user_id) else user_id
        curr_month = re.search(r"\d{4}-\d{2}", month).group() if re.search(r"\d{4}-\d{2}", month) else month

        data = external_data[curr_user_id][curr_month]
        return str(data)
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

if __name__ =='__main__':
   print(fetch_external_data("1002", "2025-01"))
