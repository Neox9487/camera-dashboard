from modules import Camera, Threshold

import threading
import cv2 as cv

class CameraManager:
  def __init__(self):
    self.cameras = {}
    self.lock = threading.Lock()
    self.avilables = self.detect_avilable_cameras()

  def detect_avilable_cameras(self, max_camera = 4):
    available = []
    for i in range(max_camera):
      cap = cv.VideoCapture(i)
      if cap is not None and cap.read()[0]:
        available.append(i)
        cap.release
    return available
  
  def get_avilable_cameras(self):
    return self.avilables
  
  def get_camera(self, id: int = 0) -> Camera:
    with self.lock:
      if id not in self.avilables:
        raise RuntimeError(f"Can't get camera ID: {id}!")
      if id not in self.cameras:
        self.cameras[id] = Camera(id)
      return self.cameras[id]
  
  def release_all(self):
    with self.lock:
      for cam in self.cameras.values():
        cam.release()
        self.cameras.clear()