from taskiq import InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from src.common.config import Config

config = Config()

if config.enable_in_memory_task_broker:
    broker = InMemoryBroker()
else:
    broker = AioPikaBroker(
        f"amqp://{config.rabbitmq_default_user}:{config.rabbitmq_default_pass}"
        f"@{config.rabbitmq_host}/"
    )

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
