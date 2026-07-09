from src.screener.engine import ScreenerEngine


class PresetScreeners:

    def __init__(self, dataframe):
        self.engine = ScreenerEngine(dataframe)

    def quality_compounder(self):

        filters = {
            "return_on_equity_pct": 15,
            "debt_to_equity": 1,
            "free_cash_flow_cr": 0,
            "operating_profit_margin_pct": 10
        }

        return self.engine.apply_filters(filters)

    def value_pick(self):

        filters = {
            "pe_ratio": 20,
            "pb_ratio": 3,
            "debt_to_equity": 2,
            "dividend_yield_pct": 1
        }

        return self.engine.apply_filters(filters)

    def growth_accelerator(self):

        filters = {
            "operating_profit_margin_pct": 15,
            "return_on_equity_pct": 20,
            "debt_to_equity": 2
        }

        return self.engine.apply_filters(filters)

    def dividend_champion(self):

        filters = {
            "dividend_yield_pct": 2,
            "free_cash_flow_cr": 0
        }

        return self.engine.apply_filters(filters)

    def debt_free_bluechip(self):

        filters = {
            "debt_to_equity": 0,
            "return_on_equity_pct": 12
        }

        return self.engine.apply_filters(filters)

    def turnaround_watch(self):

        filters = {
            "free_cash_flow_cr": 0
        }

        return self.engine.apply_filters(filters)