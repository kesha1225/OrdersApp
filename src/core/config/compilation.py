from dotenv import load_dotenv

from .app import _AppConfig
from .api import _ApiConfig
from .message_broker import _MessageBrokerConfig
from .redis import _RedisConfig

load_dotenv()

APP_CONFIG = _AppConfig()
API_CONFIG = _ApiConfig()
MessageBrokerConfig = _MessageBrokerConfig()
RedisConfig = _RedisConfig()
