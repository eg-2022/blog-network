from utils.colors import Color
from utils.format import Format

def format_text(text: str,
                color: Color = Color.NO_COLOR,
                format: Format = Format.NO_FORMAT) -> str:
    """
    This function needs a text, a color to be colorized, and a format. Only the `text` parameter
    is a required option, other ones are optional.
    """
    color_codes = {
        Color.NO_COLOR: "",
        Color.AQUA: "\033[38;5;14m",
        Color.LIME: "\033[38;5;10m",
        Color.GOLD: "\033[38;5;220m",
        Color.RED: "\033[38;5;9m"
    }
    format_codes = {
        Format.NO_FORMAT: "",
        Format.BOLD: "\033[1m",
        Format.UNDERLINED: "\033[4m",
        Format.RESET: "\033[0m"
    }

    return f"{color_codes[color]}{format_codes[format]}{text}{format_codes[Format.RESET]}"