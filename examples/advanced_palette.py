from __future__ import annotations

from functools import partial
from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, Static
from textual.containers import Vertical, Horizontal

class ColorProvider(Provider):
    """A custom provider to change the background color."""

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        colors = [
            "red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"
        ]
        
        for color in colors:
            score = matcher.match(color)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(color),
                    partial(self.app.set_background, color),
                    help=f"Set background to {color}",
                )

    def run(self, color: str) -> None:
        """Called when a hit is selected."""
        self.app.query_one("#content").styles.background = color


class ActionProvider(Provider):
    """A custom provider to trigger explicit actions."""

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        actions = {
            "Reset": self.reset_app,
            "Say Hello": self.say_hello,
        }

        for name, callback in actions.items():
            score = matcher.match(name)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(name),
                    callback,
                    help="Trigger this action",
                )

    def reset_app(self) -> None:
        self.app.query_one("#content").styles.background = "transparent"
        self.app.query_one("#status").update("Status: Ready")

    def say_hello(self) -> None:
        self.app.query_one("#status").update("Status: Hello from Command Palette!")


class CommandPaletteDemoApp(App):
    """Demonstrates custom Command Palette providers."""

    CSS = """
    #content {
        height: 1fr;
        border: solid green;
        align: center middle;
    }
    #status {
        text-align: center;
        text-style: bold;
    }
    """

    # Register the custom providers
    COMMANDS = {ColorProvider, ActionProvider}
    
    BINDINGS = [("ctrl+p", "command_palette", "Open Command Palette")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label("Press Ctrl+P to open the Command Palette", id="status"),
            id="content"
        )
        yield Footer()

    def set_background(self, color: str) -> None:
        self.query_one("#content").styles.background = color
        self.query_one("#status").update(f"Status: Background set to {color}")


if __name__ == "__main__":
    app = CommandPaletteDemoApp()
    app.run()
