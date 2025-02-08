import uvicorn

from common import AppConfig
from common.logs import init_logger

if __name__ == "__main__":
    init_logger(AppConfig())
    uvicorn.run("socketio_app:create_app", factory=True, host="0.0.0.0", port=8001)
