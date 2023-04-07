from datetime import datetime


class StringUtil:

    @staticmethod
    def get_now_string() -> str:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
