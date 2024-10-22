from time import time

level = 0
level_colors = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"]
reset_color = "\033[0m"

class TimePrint:
    def __init__(self, message: str, nice=True) -> None:
        self.message = message
        if nice:
            self.message = f"~~ {self.message} ~~"

    def __enter__(self) -> None:
        global level
        self.color = level_colors[level % len(level_colors)]
        print(self.color + self.message + reset_color)
        self.start = time()
        level += 1

    def _unit_map(self, dt: float) -> str:
        if dt < 1e-6:
            return f"{dt * 1e9:.1f} ns"
        if dt < 1e-3:
            return f"{dt * 1e6:.1f} µs"
        if dt < 1:
            return f"{dt * 1e3:.1f} ms"
        if dt < 60:
            return f"{dt:.1f} s"
        if dt < 3600:
            return f"{dt / 60:.1f} min"
        return f"{dt / 3600:.1f} h"

    def __exit__(self, *args):
        dt = time() - self.start
        print(self.color + f"done ({self._unit_map(dt)})" + reset_color)
        global level
        level -= 1
