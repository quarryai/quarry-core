import numpy as np
import pandas as pd


def cleanup_html_table_df(df: pd.DataFrame, unnamed_col_prefix: str = "unnamed_col"):
    """
    Preprocess a pandas DataFrame.

    This method should be implemented to handle any necessary preprocessing
    of the DataFrame before converting it to a dictionary.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        unnamed_col_prefix (str): Replacement prefix for no column names.
    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """

    def rename_column(col: str, idx):
        col_name: str = str(col).strip()

        if not col_name or col_name.lower().startswith("unnamed: ") or col_name == str(idx):
            return f"{unnamed_col_prefix}_{idx}"

        return col

    # Rename columns using a list comprehension
    df.columns = [rename_column(col, idx) for idx, col in enumerate(df.columns)]

    return df.replace({np.nan, None})
