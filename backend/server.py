from configs import SERVER_HOST, SERVER_PORT, API_PREFIX, WS_PREFIX, LOGGING_ERROR_FILE, LOGGING_INFO_FILE, LOGGING_FORMAT, IMAGE_SEND_FREQ
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import asyncio
import logging
import cv2 as cv

from helpers import CameraManager

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
    self.ws_prefix = WS_PREFIX

    logging.basicConfig(
      filemode='a',
      level=logging.INFO,
      format=LOGGING_FORMAT,
      datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    self.info_logger = logging.getLogger("ServerInfo")
    self.info_fh = logging.FileHandler(LOGGING_INFO_FILE)
    self.info_fh.setLevel(logging.INFO)
    self.info_fh.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    self.info_logger.addHandler(self.info_fh)

    # Error logger
    self.error_logger = logging.getLogger("ServerError")
    self.error_fh = logging.FileHandler(LOGGING_ERROR_FILE)
    self.error_fh.setLevel(logging.ERROR)
    self.error_fh.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    self.error_logger.addHandler(self.error_fh)

    self.log_info(f"Server initialized with configuration: Host: {self.host}, Port: {self.port}, API Prefix: {self.api_prefix}")

    self.camera_manager = CameraManager()

    # APIs ------

    @self.app.get(f"/")
    def root():
    # Root
      self.log_info("Root endpoint accessed")
      return {"message": "Hello, you got wrong way ヽ(･∀･)ﾉ"}
    
    @self.app.get(f"{self.api_prefix}/camera/{id}/settings")
    def get_camera_settings(id: int):
    # Get camera settings
      self.log_info(f"Getting settings for camera {id}")

    @self.app.put(f"{self.api_prefix}/camera/{id}/settings")
    def update_camera_settings(id: int, settings: dict):
    # Update camera settings
      self.log_info(f"Updating settings for camera {id} with data: {settings}")

    @self.app.websocket(f"/{self.ws_prefix}/camera/{id}")
    # Send camera frame via WebSocket
    async def camera_websocket(websocket: WebSocket, id: int):
      await websocket.accept()
      await self.send_frame(websocket, id)

    # APIs ------

  async def send_frame(self, websocket: WebSocket, id: int):
    camera = self.camera_manager.get_camera(id)
    try:
      while True:
        frame = camera.get_frame()
        ret, jpeg_frame = cv.imencode(".jpg", frame)

        if not ret:
          self.log_error("Failed to encode frame")
          raise RuntimeError("Failed to encode frame")
        
        jpeg_bytes = jpeg_frame.tobytes()

        await websocket.send_bytes(jpeg_bytes)
        await asyncio.sleep(IMAGE_SEND_FREQ)

    except Exception as e:
      self.log_error(f"Error: {e}")

    finally:
      camera.release

  def run(self):
    import uvicorn
    self.log_info(f"Server running at http://{self.host}:{self.port}{self.api_prefix}")
    uvicorn.run(self.app, host=self.host, port=self.port)

  def log_info(self, message: str):
    self.info_logger.info(message)
    self.info_fh.flush()

  def log_error(self, message: str):
    self.error_logger.error(message)
    self.error_fh.flush()

