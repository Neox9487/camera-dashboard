import threading
import cv2 as cv

#  "exposure": 100,
#  "black_level": 0, # 0 ~ 40,
#  "gain": 0, # 0 ~ 45,
#  "red_balance": 0, # 0 ~ 2500,
#  "blue_balance": 0, # 0 ~ 2500, 
#  "color_threshold": {
#    "hue_min": 0,
#    "hue_max": 180,
#    "sat_min": 0,
#    "sat_max": 255,
#    "val_min": 0,
#    "val_max": 255,
#  }

class Threshold:
  hue_min: int
  hue_max: int
  sat_min: int
  sat_max: int
  val_min: int
  val_max: int

class Camera:
  def __init__(self, camera_id=0):
    self.camera_id = camera_id
    self.cap = None
    self.lock = threading.Lock()
    self._ensure_camera()

    self.mode = "color"
    self.exposure = 100
    self.black_level = 0
    self.red_balance = 1200
    self.blue_balance = 1200
    self.threshold = Threshold
    self.threshold.hue_min = 180
    self.threshold.hue_min = 0
    self.threshold.sat_min = 255
    self.threshold.sat_min = 0
    self.threshold.val_min = 255
    self.threshold.val_min = 0

  def set(
    self,
    mode: str,
    exposure: int,
    black_level: int,
    red_balance: int,
    blue_balance: int,
    threshold: Threshold
  ):
  # set values
    self.mode = mode
    self.exposure = exposure
    self.black_level =black_level
    self.red_balance = red_balance
    self.blue_balance = blue_balance
    self.threshold = threshold    

  def _ensure_camera(self):
    if self.cap is None or not self.cap.isOpened():
      self.release()
      self.cap = cv.VideoCapture(self.camera_id)

  def get_frame(self):
    with self.lock:
      self._ensure_camera()
      if self.cap is None or not self.cap.isOpened():
        raise RuntimeError("Camera not available")
      ret, frame = self.cap.read()
      if not ret or frame is None:
        raise RuntimeError("Failed to read frame (camera may be unplugged)")
      return frame

  def release(self):
    if self.cap is not None:
      self.cap.release()
      self.cap = None