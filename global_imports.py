import os
from rich.console import Console
from rich.theme import Theme
from shutil import get_terminal_size

os.chdir(os.path.dirname(os.path.abspath(__file__)))

console = Console(theme=Theme(
    {
        "normal1"    :   "bold blue1",
        "normal2"    :   "bold dark_violet",

        "warning1"   :   "bold plum4",
        "warning2"   :   "bold red",
    }))


def display_progress_bar(archived_count: int, total_count: int, item_name: str, char_fill = "█", scale = 0.55) -> None:
    """
    Description:
        Displays a progress bar.
    ---
    Parameters:
        `archived_count` (`int`)
            An integer representing the number of the files that have been archived.
        
        `total_count` (`int`)
            An integer representing the total number of files that are being archived.
        
        `item_name` (`str`)
            The name of downloading item.
        
        `char_fill` (`str`)
            The character representing the downloaded pieces to fill the progress bar with.
        
        `scale` (`float`)
            The percentage at which the progress bar should be taking from the terminal window.
    ---
    Returns: `None`.
    """
    
    columns          = get_terminal_size().columns
    max_width        = int(columns * scale)
    text_max_length  = int(columns * (1 - scale - 0.32))
    
    filled           = int(round(max_width * archived_count / float(total_count)))
    remaining        = max_width - filled
    progress_bar     = char_fill * filled + " " * remaining
    percent          = round(100.0 * archived_count / float(total_count), 2)
    
    text     = f"[normal1][normal2]{item_name[:text_max_length]:<{text_max_length}}[/] | \[[normal2]{archived_count:<3}[/]/[normal2]{total_count:>3}[/]] | [normal2]{progress_bar}[/] |[normal2]{percent:< 7.2f}[/] %[/]"
    
    # if len(item_name) > columns - max_width - 10:
        # text     = f"[normal1][normal2]{item_name[:columns-max_width-5]}[/] | \[[normal2]{archived_count:<3}[/]/[normal2]{total_count:>3}[/]] | [normal2]{progress_bar}[/] |[normal2]{percent:< 7.2f}[/] %[/]"
    console.print(text, end="")
    print("\r", end="")
