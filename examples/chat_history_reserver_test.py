from enum import StrEnum
from pydantic import BaseModel
from uuid import uuid4
from chat_history_reserver.database import DictDatabase



class Role(StrEnum):
    USER = "User"
    ASSISTANT = "Assistant"
    SYSTEM = "System"


class ChatModel(BaseModel):
    role: Role
    message: str



if __name__ == "__main__":
    db = DictDatabase()
    db.set_model(ChatModel)
    conversation_id = uuid4()
    db.create_history(conversation_id)
    for i in range(10):
        db.add_chat(conversation_id, ChatModel(role=Role.USER, message=f"hello {i}"))
    print(db.get_history(conversation_id))
    db.dump(conversation_id, "json", "out.json")
    db.dump(conversation_id, "csv", "out.csv")
