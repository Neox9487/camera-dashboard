from module import Json

# camera_setting_module = {
#   "1": {
#     "last_pipeline": "pipeline1",
#     "pipelines": {
#       "pipeline1": {
#         "mode": "color" # or "apriltag",
#         "exposure": 100,
#         "black_level": 0, # 0 ~ 40,
#         "gain": 0, # 0 ~ 45,
#         "red_balance": 0, # 0 ~ 2500,
#         "blue_balance": 0, # 0 ~ 2500, 
#         "color_threshold": {
#           "hue_min": 0,
#           "hue_max": 180,
#           "sat_min": 0,
#           "sat_max": 255,
#           "val_min": 0,
#           "val_max": 255,
#        }
#      },
#      "pipeline2": {
#         ......
#      },
#      ...... # 8 pipelines
#   },
#   "2": {
#     ......
#   },
#   ...... # 4 cameras
# }

# 4 cameras, 8 pipelines each

class API:
  @staticmethod
  def get_all_cameras_settings() -> dict:
  # get camera settings 
    pass

  @staticmethod
  def update_camera_settings(id: int, pipeline: str, settings: dict) -> None:
  # update camera settings by id and pipeline
    pass

  @staticmethod
  def to_default_camera_settings(id: int, pipeline: str) -> None:
  # reset camera settings to default by id and pipeline
    pass