import json
import os
import traceback
import inspect
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "LOGS")
LOG_FILE = os.path.join(LOG_DIR, "error.json")

class ErrorHandler:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    def write_log(self, level, class_name, function_name, message, e=None):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = []

            log = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "level": level,
                "class": class_name,
                "function": function_name,
                "message": str(message)
            }

            if e:
                tb = traceback.extract_tb(e.__traceback__)[-1]
                log["line"] = tb.lineno
                log["file"] = tb.filename

            data.append(log)

            with open(LOG_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except Exception:
            pass

    def get_location(self):
        frame = inspect.currentframe().f_back
        while frame:
            if not frame.f_code.co_filename.endswith("error_hendal.py"):
                obj = frame.f_locals.get("self")
                return (
                    obj.__class__.__name__ if obj else None,
                    frame.f_code.co_name
                )
            frame = frame.f_back
        return None, None

    def warning(self, message):
        class_name, function_name = self.get_location()
        print(message)
        self.write_log("WARNING", class_name, function_name, message)

    def error(self, message):
        class_name, function_name = self.get_location()
        print(message)
        self.write_log("ERROR", class_name, function_name, message)

    def exception(self, e):
        class_name, function_name = self.get_location()
        self.write_log("EXCEPTION", class_name, function_name, e, e)

    def log_warning(self, class_name, function_name, message):
        self.write_log("WARNING", class_name, function_name, message)

    def log_error(self, class_name, function_name, message):
        self.write_log("ERROR", class_name, function_name, message)

    def log_exception(self, class_name, function_name, e):
        self.write_log("EXCEPTION", class_name, function_name, e, e)


error_handler = ErrorHandler()