# Refrigerator-LangChain-ReAct-Agent

# 📘 智能冰箱客服 Agent（LangChain 实现）

一个基于 **LangChain + ReAct Agent + RAG** 的智能客服系统，支持：

* 🤖 多工具调用（天气 / 用户信息 / 外部数据）
* 📊 自动生成用户使用报告
* 📚 RAG 知识检索增强
* 💬 Streamlit 可视化聊天界面

---

# 🚀 项目效果

* 类似 ChatGPT 的对话界面
* 支持工具调用（自动获取用户ID、月份、数据等）
* 自动生成“用户使用报告”

---

# 🧱 技术架构

```text
Streamlit 前端
    ↓
LangChain Agent（ReAct）
    ↓
Tools（工具函数）
    ↓
RAG / 外部数据
```

---

# 📦 环境配置

## 1️⃣ 创建虚拟环境

```bash
conda create -n agent python=3.10 -y
conda activate agent
```

---

## 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

---

# 🔑 API Key 配置

本项目依赖两个外部服务：

---

## ✅ 1. 阿里云通义千问（DashScope）

👉 获取地址：
👉 [https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)

设置环境变量：

### Windows（PowerShell）

```bash
$env:DASHSCOPE_API_KEY="你的API_KEY"
```

### Linux / Mac

```bash
export DASHSCOPE_API_KEY="你的API_KEY"
```

---

## ✅ 2. 高德地图 API（用于天气/位置服务）

👉 获取地址：
👉 [https://console.amap.com/dev/key/app](https://console.amap.com/dev/key/app)

> ⚠️ 如果你没有用到真实天气接口，可以暂时不配置

---

# ▶️ 启动项目

```bash
streamlit run app.py
```

启动后浏览器打开：

```text
http://localhost:8501
```

---

# 💬 使用说明

你可以输入类似：

* “给我生成我的使用报告”
* “我这个月使用情况怎么样？”
* “帮我分析一下我的设备效率”

Agent 会自动：

1. 获取用户ID
2. 获取当前月份
3. 查询外部数据
4. 调用 RAG
5. 生成完整报告

---

# 🧰 工具说明（Agent Tools）

| 工具名                       | 作用        |
| ------------------------- | --------- |
| `get_user_id`             | 获取用户ID    |
| `get_user_location`       | 获取用户所在城市  |
| `get_current_month`       | 获取当前月份    |
| `get_weather`             | 查询天气      |
| `fetch_external_data`     | 查询用户历史数据  |
| `rag_summarize`           | 知识库总结     |
| `fill_context_for_report` | 触发报告生成上下文 |

---

# 📁 项目结构

```text
.
├── agent/
│   ├── react_agent.py        # Agent 核心逻辑
│   └── tools/
│       ├── agent_tools.py    # 工具函数
│       └── middleware.py     # 中间件（日志/提示词切换）
│
├── rag/
│   └── rag_service.py        # RAG 检索服务
│
├── utils/
│   ├── config_handler.py     # 配置读取
│   ├── logger_handler.py     # 日志工具
│   └── path_tool.py          # 路径处理
│
├── app.py                    # Streamlit 前端
├── requirements.txt          # 依赖
└── README.md                 # 项目说明
```

---

# ⚠️ 常见问题（FAQ）

---

## ❓1. 报错：API Key missing

👉 原因：没有配置环境变量

解决：

```bash
$env:DASHSCOPE_API_KEY="你的key"
```

---

## ❓2. Tool 报错参数问题

```text
takes 0 positional arguments but 1 was given
```

👉 原因：工具函数必须写成：

```python
def xxx(input: str) -> str:
```

---

## ❓3. Agent 不调用工具

👉 原因：

* Tool 名字不清晰
* Prompt 不明确

👉 建议使用英文 tool 名：

```python
get_user_id
get_weather
```

---

## ❓4. Streamlit 不刷新 / 无输出

👉 解决：

```python
st.rerun()
```

---

# 🧠 项目亮点（可写简历）

* ✔ 基于 ReAct 架构的智能 Agent
* ✔ 多工具自动调用链路
* ✔ RAG + 外部数据融合
* ✔ 类 ChatGPT 流式交互界面
* ✔ 可扩展为企业级智能客服

---

# 📌 后续可扩展方向

* 🔄 接入真实天气 API（高德）
* 📊 报告可视化（图表）
* 🧠 升级 LangGraph（支持多 Agent）
* 🌐 部署为 Web 服务（FastAPI）

---

# ⭐ 如果这个项目对你有帮助

欢迎 ⭐ Star 支持一下！

---

# 🧾 License

MIT License

---
