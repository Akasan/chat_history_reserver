from langchain_core.prompts import ChatPromptTemplate
from enum import StrEnum
from pydantic import BaseModel
from abc import ABC, abstractmethod



class DumpFormat(StrEnum):
    CSV = "csv"
    JSON = "json"


class IDatabase(ABC):
    @abstractmethod
    def create_history(self, conversation_id: str):
        pass

    @abstractmethod
    def add_chat(self, conversation_id: str, chat: str):
        pass

    @abstractmethod
    def get_history(self, conversation_id: str) -> list[str]:
        pass

    @abstractmethod
    def delete_history(self, conversation_id: str):
        pass

    @abstractmethod
    def set_model(self, model: BaseModel):
        pass

    @abstractmethod
    def dumps(self, conversation_id: str, format: DumpFormat) -> str:
        pass

    @abstractmethod
    def dump(self, conversation_id: str, format: DumpFormat, filename: str) -> str:
        pass

    @abstractmethod
    def to_chat_prompt_template(self, conversation_id: str) -> ChatPromptTemplate:
        pass
