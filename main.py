from src.crawler_data_fields import CBot
from src.test_api import Simulate_API
from src.generate_alpha import Alpha_Generator
import argparse

def _crawler(opt):
    bot = CBot()
    # url = "https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity"
    # save_path = "Price Volume Data for Equity.csv"
    url = opt.url
    save_path = opt.save_path
    bot.crawler(url=url, save_path=save_path) 

def _combine_alpha(opt):
    alpha_generator = Alpha_Generator()
    simAPI = Simulate_API()
    list_alpha = [
            "rank(-ts_delta(cap,2))",
            "-(low-close)^3*(open^7) / (low-high)^3 / (close^7)",
            # "adv20/sharesout+returns",
            "rank(trade_when(adv20>volume, -returns, -1))"
            ]
    field_neutralization = opt.neutralize
    alpha = alpha_generator.combine_alpha(list_alpha, field_neutralization=field_neutralization)
    metric, _ = simAPI.simulate(alpha)
    print(metric)

def _generate_alpha(opt):
    alpha_generator = Alpha_Generator()
    formula_template = "-ts_zscore({0}/{1}, 30)"
    n_variable = 2
    alpha_generator.generate(formula=formula_template, num_variable=n_variable, dataset=opt.dataset)

def main(opt):
    if opt.tool =='crawl':
        _crawler(opt)
    elif  opt.tool =='gen':
        _generate_alpha(opt)
    elif opt.tool =='combine':
        _combine_alpha(opt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="World Quant Brain Tools for Crawl Data Fields, Generate/Combine Alpha and Simulate")

    parser.add_argument('--tool', '-t', choices=['crawl', 'gen', 'combine'], default='gen',\
                         help="Tool Option Crawl-crawl/Generate-gen/Combine-combine")

    parser.add_argument('--url', '-u', type=str, default="https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity",\
                          help="URL to dataset page")
    parser.add_argument('--save_path', '-p',  type=str, default="Price Volume Data for Equity.csv",\
                          help="Path to save csv file")
    parser.add_argument('--neutralize', '-f', default=None,\
                         help="Field to Neutralize <industry/subindustry/market/sector>")
    parser.add_argument('--dataset', '-d', default='price_volume',\
                         help="Dataset <'price_volume'/fundamental_datasets>")     

    opt = parser.parse_args()
    main(opt)