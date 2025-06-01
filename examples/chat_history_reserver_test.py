from pprint import pprint
from enum import StrEnum
from pydantic import BaseModel
from uuid import uuid4
from chat_history_reserver.database import DictDatabase



class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatModel(BaseModel):
    role: Role
    message: str



if __name__ == "__main__":
    db = DictDatabase()
    db.set_model(ChatModel)
    conversation_id = uuid4()
    db.create_history(conversation_id)
    for i in range(10):
        db.add_chat(conversation_id, ChatModel(role=Role.USER if i % 2 == 0 else Role.ASSISTANT, message=f"hello {i}" + "{hoge}"))
    chats = db.to_chat_prompt_template(conversation_id)
    print(chats.invoke({"hoge": "fuga"}))
