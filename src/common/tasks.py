from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from src.common.config import Config

config = Config()

broker = AioPikaBroker(
    f"amqp://{config.rabbitmq_username}:{config.rabbitmq_password}"
    f"@{config.rabbitmq_host}/"
)

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
