import pandas as pd
from support.constants import NC_FP
from support.types import PendulumEntry

ORIENT_MODE = "index"


def extract_and_convert(relative_filepath: str) -> list[PendulumEntry]:
    """
    Creates a list of pendula given a CSV file.

    Args:
        relative_filepath (str): filepath to access CSV with pendula data

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes

    """
    df = pd.read_csv(relative_filepath)  # type: ignore
    bad_rep = df.to_dict(orient=ORIENT_MODE)  # type: ignore
    good_rep = []

    for key in bad_rep:
        good_rep.append(bad_rep[key])
    return good_rep


# Provided


def write_to_csv(pend_list: list[PendulumEntry]) -> None:
    """
    Writes a pend_list to the Newton's Cradle CSV file called "newton_cradle_pends.csv"

    Args:
        pend_list (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes
    """
    df = pd.DataFrame.from_dict(pend_list)  # type: ignore
    df.to_csv(NC_FP, index=False)
