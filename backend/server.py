from configs import SERVER_HOST, SERVER_PORT, API_PREFIX, LOGGING_LEVEL, LOGGING_FORMAT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

class Server:
  def __init__(self):
    self.app = FastAPI()
    self.app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["GET", "PUT"],
      allow_headers=["*"],
    )
    self.host = SERVER_HOST
    self.port = SERVER_PORT
    self.api_prefix = API_PREFIX

    logging.basicConfig(
      filemode='a',
      level=LOGGING_LEVEL,
      format=LOGGING_FORMAT,
      datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    self.logger = logging.getLogger("Server")
    self.fh = logging.FileHandler("server.log")
    self.fh.setLevel(LOGGING_LEVEL)
    self.fh.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    self.logger.addHandler(self.fh)

    self.log(f"Server initialized with configuration: Host: {self.host}, Port: {self.port}, API Prefix: {self.api_prefix}")

    @self.app.get(f"/")
    def root():
    # Root
      self.log("Root endpoint accessed")
      return {"message": "Hello, you got wrong way ヽ(･∀･)ﾉ"}
    
    @self.app.get(f"{self.api_prefix}/camera/{id}/settings")
    def get_camera_settings(id: int):
    # Get camera settings
      self.log(f"Getting settings for camera {id}")

    @self.app.put(f"{self.api_prefix}/camera/{id}/settings")
    def update_camera_settings(id: int, settings: dict):
    # Update camera settings
      self.log(f"Updating settings for camera {id} with data: {settings}")

    @self.app.websocket(f"{self.api_prefix}/camera/{id}/ws")
    # Send camera images and target points via WebSocket
    async def camera_websocket(websocket, id: int):
      pass

  def run(self):
    import uvicorn
    self.log(f"Server running at http://{self.host}:{self.port}{self.api_prefix}")
    uvicorn.run(self.app, host=self.host, port=self.port, log_level=LOGGING_LEVEL.lower())

  def log(self, message: str):
    self.logger.info(message)
    self.fh.flush()

