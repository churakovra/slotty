import logging
from dataclasses import dataclass

from app.message.context import AbstractBotMessageContext

logger = logging.getLogger(__name__)


@dataclass
class MessageRecipient:
    chat_id: int


@dataclass
class MessagePack:
    message_context: AbstractBotMessageContext
    message_recipients: list[MessageRecipient]

    def to_dict(self):
        result = {
            "message_context": self.message_context.to_dict(),
            "message_recipients": [recipient.__dict__ for recipient in self.message_recipients],
        }
        logger.debug(result)
        return result
