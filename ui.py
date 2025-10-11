#!/usr/bin/env python

from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Digits

# TODO:
"""
- Display status of UserGameSettings.ini file
- Display current parsed:
    - VHS Tapes
    - Cartridges
    - Gameboys
"""

# Future TODO:
"""
- Display status of Cassette Tapes
"""

class ClockApp(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Digits("")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")

if __name__ == "__main__":
    app = ClockApp()
    app.run()
