import logging

import uvicorn
from alembic import command
from alembic.config import Config

from src.config.server import server_settings
from src.infrastructure.fastapi.app import create_app
from src.infrastructure.logger.logger import LoggerConfig


def main() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    # logging.basicConfig(level=logging.DEBUG)
    LoggerConfig.setup_logger()

    logging.info("Creating FastAPI app...")
    app = create_app()

    logging.info("Running uvicorn server...")
    uvicorn.run(
        app,
        host=server_settings.HOST,
        port=server_settings.PORT
    )
