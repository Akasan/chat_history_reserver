from langchain_core.prompts import ChatPromptTemplate
import json
from pydantic import BaseModel
from .interface import IDatabase, DumpFormat


class DictDatabase(IDatabase):
    def __init__(self):
        super().__init__()
        self._db = {}
        self._model = None

    def create_history(self, conversation_id: str):
        self._db[conversation_id] = []

    def add_chat(self, conversation_id: str, chat: BaseModel):
        if not conversation_id in self._db:
            raise IndexError(f"{conversation_id} does not exist.")
        if not isinstance(chat, self._model):
            raise ValueError(f"Please set chat as {self._model}")

        self._db[conversation_id].append(chat)

    def get_history(self, conversation_id: str) -> list[str]:
        if not conversation_id in self._db:
            raise IndexError(f"{conversation_id} does not exist.")

        return self._db[conversation_id]

    def delete_history(self, conversation_id: str):
        if not conversation_id in self._db:
            raise IndexError(f"{conversation_id} does not exist.")

        return self._db[conversation_id]

    def set_model(self, model: BaseModel):
        self._model = model

    def dumps(self, conversation_id: str, format: DumpFormat) -> str:
        schema = tuple(self._model.schema()["properties"].keys())

        if format == DumpFormat.CSV:
            text = ",".join(schema) + "\n"

            for history in self._db[conversation_id]:
                history_dict = history.dict()
                text += ",".join(history_dict[k] for k in schema) + "\n"

            return text
        elif format == DumpFormat.JSON:
            result = [history.dict() for history in self._db[conversation_id]]
            return json.dumps(result)

    def dump(self, conversation_id: str, format: DumpFormat, filename: str):
        if format == DumpFormat.CSV:
            text = self.dumps(conversation_id, format)
            with open(filename, "w") as f:
                f.write(text)
        elif format == DumpFormat.JSON:
            with open(filename, "w", encoding="utf-8") as f:
                result = [history.dict() for history in self._db[conversation_id]]
                json.dump(result, f, indent=2)

    def to_chat_prompt_template(self, conversation_id: str) -> ChatPromptTemplate:
        items = [item.dict() for item in self._db[conversation_id]]
        prompt = ChatPromptTemplate.from_messages(
            [
                (item["role"], item["message"]) for item in items
            ]
        )
        return prompt
