import pandas as pd
import numpy as np

from .basic import BasicAnalyzer

class overlap():
    @staticmethod
    def DEMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        str_obj = dataframe.columns.str
        if str_obj.contains(pat="^EMA", regex=True).sum() == 0:
            dataframe.pipe(
                BasicAnalyzer.EMA,
                interval=interval,
                target_col=target_col,
            )
        dataframe.pipe(
            BasicAnalyzer.EMA,
            interval=interval,
            target_col=f"EMA_{interval}",
            is_EMA_of_EMA=True,
        )

        dataframe[f"DEMA_{interval}"] = (
            2 * dataframe[f"EMA_{interval}"] - dataframe[f"EMA_of_EMA_{interval}"]
        )
        return dataframe

    @staticmethod
    def TEMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        str_obj = dataframe.columns.str
        if str_obj.contains(pat="^EMA", regex=True).sum() == 0:
            (
                dataframe.pipe(
                    BasicAnalyzer.EMA,
                    interval=interval,
                    target_col=target_col,
                ).pipe(
                    BasicAnalyzer.EMA,
                    interval=interval,
                    target_col=f"EMA_{interval}",
                    is_EMA_of_EMA=True,
                )
            )

        elif str_obj.contains(pat="^EMA_\d", regex=True).sum() == 1:
            dataframe.pipe(
                BasicAnalyzer.EMA,
                interval=interval,
                target_col=f"EMA_{interval}",
                is_EMA_of_EMA=True,
            )

        dataframe.pipe(
            BasicAnalyzer.EMA,
            interval=interval,
            target_col=f"EMA_of_EMA_{interval}",
            is_EMA_of_EMA=True,
        )

        dataframe[f"DEMA_{interval}"] = (
            3 * dataframe[f"EMA_{interval}"]
            - 3 * dataframe[f"EMA_of_EMA_{interval}"]
            - dataframe[f"EMA_{interval}"]
        )