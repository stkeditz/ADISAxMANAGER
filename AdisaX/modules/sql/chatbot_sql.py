import threading

from sqlalchemy import Column, String

from AdisaX.modules.sql import BASE, SESSION


class DILXCHATS(BASE):
    __tablename__ = "dilx_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


DILXCHATS.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_adisa(chat_id):
    try:
        chat = SESSION.query(DILXCHATS).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_adisa(chat_id):
    with INSERTION_LOCK:
        dilxchat = SESSION.query(DILXCHATS).get(str(chat_id))
        if not dilxchat:
            dilxchat = DILXCHATS(str(chat_id))
        SESSION.add(dilxchat)
        SESSION.commit()


def rem_adisa(chat_id):
    with INSERTION_LOCK:
        dilxchat = SESSION.query(DILXCHATS).get(str(chat_id))
        if dilxchat:
            SESSION.delete(dilxchat)
        SESSION.commit()
