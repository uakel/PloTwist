from .program import Item, ChangeStacker
import plotwist as ptw

def title(title: str) -> None:
    """
    Add a title to the html report.

    Args:
        title: str, the title of the report

    Returns:
        None
    """
    item = Item(f"<h1>{title}</h1>", mode="block")
    ptw.program.append(item)

def subtitle(subtitle: str) -> None:
    """
    Add a subtitle to the html report.

    Args:
        subtitle: str, the subtitle of the report

    Returns:
        None
    """
    item = Item(f"<h2>{subtitle}</h2>", mode="block")
    ptw.program.append(item)

def stacker(stacker: str) -> None:
    """
    Change the stacker of the html report.

    Args:
        stacker: str, the stacker type

    Returns:
        None
    """
    stackfluencer = ChangeStacker(stacker)
    ptw.program.append(stackfluencer)

def comment(comment: str) -> None:
    """
    Add a comment to the html report.

    Args:
        comment: str, the comment

    Returns:
        None
    """
    item = Item(f"<p>{comment}</p>", mode="block")
    ptw.program.append(item)

def rule() -> None:
    """
    Add a horizontal rule to the html report.

    Args:
        None

    Returns:
        None
    """
    item = Item("<hr>", mode="block")
    ptw.program.append(item)

from .plot import type_one_comparative, density_from_percentiles, nth_listvalued_of_all_subkeys, plot
