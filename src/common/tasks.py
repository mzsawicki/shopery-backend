from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler

from src.common.config import Config

config = Config()

broker = AioPikaBroker(
    f"amqp://guest:guest"
    f"@{config.rabbitmq_host}/"
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)]
)
