from utils import Color, Format, format_text

def stage(stage_number: int, text: str) -> str:
    """
    Informs the user which stage the program is right now.
    Provide an stage number using the `stage_number` parameter and
    the necessary context in the `text` parameter.
    """
    stage_title = format_text(f"STAGE #{stage_number}:", Color.GOLD, Format.BOLD)
    text = format_text(text, Color.GOLD)
    return f"{stage_title} {text}"

def info(text: str) -> str:
    """
    Informs the user before an action triggers on the script,
    only provide the necessary context in the `text` parameter. 
    """
    info_prefix = format_text("[INFO]", Color.AQUA, Format.BOLD)
    return f"{info_prefix} {text}"

def success(text: str) -> str:
    """
    Informs the user after an action triggered **successfully** on the script,
    only provide the necessary context in the `text` parameter. 
    """
    info_prefix = format_text("[SUCCESS]", Color.LIME, Format.BOLD)
    return f"{info_prefix} {text}"

def error(text: str) -> str:
    """
    Informs the user after an action triggered **unsuccessfully** on the script,
    only provide the necessary context in the `text` parameter. 
    """
    info_prefix = format_text("[ERROR]", Color.RED, Format.BOLD)
    return f"{info_prefix} {text}"
