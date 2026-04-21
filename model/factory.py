from abc import ABC, abstractmethod
from typing import Optional
import os

from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi

from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # 优先读取环境变量，没有就用内嵌（临时方案）
        api_key = os.getenv("DASHSCOPE_API_KEY") or "sk-5b67306501ae41779f0ea6ea1b49710f"

        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置，请检查环境变量或代码")

        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=api_key
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # 同样为 Embedding 模型提供 API Key
        api_key = os.getenv("DASHSCOPE_API_KEY") or "sk-5b67306501ae41779f0ea6ea1b49710f"

        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置，请检查环境变量或代码")

        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=api_key
        )


# 初始化模型（全局单例）
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()