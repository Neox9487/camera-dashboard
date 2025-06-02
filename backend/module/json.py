import json
import orjson

class Json:
  @staticmethod
  def dumps(data: dict) -> str:
    return orjson.dumps(data).decode("utf-8")

  @staticmethod
  def loads(data: str) -> dict:
    return orjson.loads(data)
  
  @staticmethod
  def dump(data: dict, file) -> None:
    with open(file, "wb") as f:
      f.write(orjson.dumps(data))

  @staticmethod
  def load(file_path) -> dict:
    with open(file_path, "rb") as f:
      return orjson.loads(f.read())
  
  @staticmethod
  def pretty_dump(file_path: str, data: dict) -> str:
    with open(file_path, "w") as file:
      json.dump(data, file, indent=2, ensure_ascii=False)
