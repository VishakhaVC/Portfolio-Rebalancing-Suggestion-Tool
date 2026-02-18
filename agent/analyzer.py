import pandas as pd

class PortfolioAnalyzer:
    def __init__(self, data):
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        else:
            self.df = data

    def analyze(self):
        total_value = self.df["Current_Value"].sum()
        self.df["Current_Weight"] = self.df["Current_Value"] / total_value
        self.df["Drift"] = self.df["Current_Weight"] - self.df["Target_Allocation"]

        return {
            "total_value": total_value,
            "portfolio_table": self.df
        }