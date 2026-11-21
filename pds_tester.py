import pandas as pd
from src.pds_helper import extract_and_convert
from support.constants import NC_FP

# Provided
if __name__ == "__main__":
    print(pd.read_csv(NC_FP))
    print(extract_and_convert(NC_FP))