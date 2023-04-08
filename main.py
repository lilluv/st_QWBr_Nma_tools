from src.crawler_data_fields import CBot
from src.test_api import Simulate_API
from src.generate_alpha import generator

if __name__ == '__main__':

    # bot = CBot()
    # url = "https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity"
    # save_path = "Price Volume Data for Equity.csv"
    # bot.crawler(url=url, save_path=save_path)

    simAPI = Simulate_API()
    # alpha = 'delta(close,5)'
    # simAPI.simulate(alpha)

    list_alpha = [
        "rank(-ts_delta(close,2))",
        # " (close>ts_sum(close,20) / 20 ? 1.5 * rank(-ts_delta(close,2)) : rank(-ts_delta(close,2)))",
        "ts_sum(sign(ts_delta(close,1)),4) == -4 ? 0 : rank(-ts_delta(close,2))",
        "-rank(ts_delta(close,2))*rank(volume/ts_sum(volume,30)/30)",
        "volume > adv20 ? 2*rank(-ts_delta(close,2)) : rank(-ts_delta(close,2))",
        "-(low-close)^3*(open^7) / (low-high)^3 / (close^7)",
        # "rank(ts_delay(close,2)-ts_regression(close,vwap,60,lag=0,rettype=3))"
        ]
    alpha = generator(list_alpha)
    # alpha = "scale(group_neutralize(rank(-ts_delta(close,2)), industry))"
    simAPI.simulate(alpha)