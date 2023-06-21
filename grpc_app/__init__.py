import logging
import os
from concurrent import futures
from typing import Optional

from grpc.aio import server

from config import AppConfig, init_logger
from domains import init_domains
from grpc_app.generated.books_pb2_grpc import add_BooksServicer_to_server
from grpc_app.servicers.books import BooksServicer
from storage import init_storage


# TODO: Add asyncio support: https://stackoverflow.com/questions/38387443/how-to-implement-a-async-grpc-python-server
def create_server(test_config: Optional[AppConfig] = None):
    app_config = test_config or AppConfig()
    init_logger(app_config)
    init_domains(app_config)
    init_storage()
    s = server(futures.ThreadPoolExecutor(max_workers=10))
    # Register service
    add_BooksServicer_to_server(BooksServicer(), s)
    address = "0.0.0.0:9999"
    logging.info(f"[{os.getpid()}] Listening on {address}")
    s.add_insecure_port(address)
    return s


async def main():  # pragma: no cover
    s = create_server()
    await s.start()
    logging.info("GRPC started")
    await s.wait_for_termination()
