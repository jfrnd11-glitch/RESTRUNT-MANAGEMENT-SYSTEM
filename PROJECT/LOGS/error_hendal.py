import json
import os
from datetime import datetime
import traceback
import inspect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "LOGS")
LOG_FILE = os.path.join(LOG_DIR, "error.json")

class ErrorHandler:

    def __init__(self):

        os.makedirs(LOG_DIR, exist_ok=True)
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    def write_log(self, log_data):

        try:

            with open(LOG_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            data.append(log_data)

            with open(LOG_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except Exception:
            pass

    def get_location(self):

        try:

            frame = inspect.currentframe()

            while frame:

                filename = frame.f_code.co_filename

                if "error_hendal.py" not in filename:

                    function_name = frame.f_code.co_name

                    class_name = None

                    if "self" in frame.f_locals:

                        class_name = frame.f_locals["self"].__class__.__name__

                    return class_name, function_name

                frame = frame.f_back

        except Exception:
            pass

        return None, None

    def warning(self, message):

        class_name, function_name = self.get_location()

        print(message)

        log_data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": "WARNING",
            "class": class_name,
            "function": function_name,
            "message": message,
        }

        self.write_log(log_data)

    def error(self, message):

        class_name, function_name = self.get_location()

        print(message)

        log_data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": "ERROR",
            "class": class_name,
            "function": function_name,
            "message": message,
        }

        self.write_log(log_data)

    def exception(self, e):

        class_name, function_name = self.get_location()

        tb = traceback.extract_tb(e.__traceback__)[-1]

        log_data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": "EXCEPTION",
            "class": class_name,
            "function": function_name,
            "message": str(e),
            "line": tb.lineno,
            "file": tb.filename,
        }

        self.write_log(log_data)

    def log_error(self, class_name, function_name, message):

        log_data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": "ERROR",
            "class": class_name,
            "function": function_name,
            "message": message,
        }

        self.write_log(log_data)

    def log_exception(self, class_name, function_name, e):

        tb = traceback.extract_tb(e.__traceback__)[-1]

        log_data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": "EXCEPTION",
            "class": class_name,
            "function": function_name,
            "message": str(e),
            "line": tb.lineno,
            "file": tb.filename,
        }

        self.write_log(log_data)


error_handler = ErrorHandler()