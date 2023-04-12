from src.crawler_data_fields import CBot
from src.test_api import Simulate_API
from src.generate_alpha import Alpha_Generator
import argparse
import sys

class WorldQuantTool(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="World Quant Brain Tools for Crawl Data Fields, Generate/Combine Alpha and Simulate",
            usage='''main <command> [<args>]

                    The most commonly used commands are:
                    gen     Generate Alpha from String Fomula 
                    combine      Combine A List Alpha to 1 alpha and show performence
                    crawl   Crawl Data Fields from dataset page
                    ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def crawl(self):
        crawl_parser = argparse.ArgumentParser(
            description='Crawler Data Field Tool from dataset page into csv')
        crawl_parser.add_argument('--url', '-u', type=str, default="https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity",\
                        help="URL to dataset page")
        crawl_parser.add_argument('--save_path', '-p',  type=str, default="Price Volume Data for Equity.csv",\
                        help="Path to save csv file")
        args = crawl_parser.parse_args(sys.argv[2:])
        bot = CBot()
        # url = "https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity"
        # save_path = "Price Volume Data for Equity.csv"
        url = args.url
        save_path = args.save_path
        bot.crawler(url=url, save_path=save_path) 

    def gen(self):
        generate_parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        generate_parser.add_argument('--dataset', '-d', default='price_volume',\
                        help="Dataset <'price_volume'/fundamental_datasets>") 
        generate_parser.add_argument('--formula', '-f', default=None,\
                        help="Alpha Fomular String")  
        generate_parser.add_argument('--nvar', '-n', default=None,\
                        help="Number of variable")   
        args = generate_parser.parse_args(sys.argv[2:])

        alpha_generator = Alpha_Generator()
        formula_template = "-ts_zscore({0}/{1}, 30)" if not args.formula else args.formula
        n_variable = 2 if not args.nvar else args.nvar
        alpha_generator.generate(formula=formula_template, num_variable=n_variable, dataset=args.dataset)

    def combine(self):
        combine_parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        combine_parser.add_argument('--neutralize', '-f', default=None,\
                         help="Field to Neutralize <industry/subindustry/market/sector>")  
        args = combine_parser.parse_args(sys.argv[2:])
        
        alpha_generator = Alpha_Generator()
        list_alpha = [
                "rank(-ts_delta(cap,2))",
                "adv20/sharesout+returns",
                "rank(trade_when(volume < adv20, -returns, -1))",
                "assets/fnd6_cshr"
                ]
        alpha, metric, success = alpha_generator.combine_alpha(list_alpha, field_neutralization=args.neutralize)
        print("\n Alpha:\n \t", alpha)
        print(">--{0}--<".format("PASS" if success else "FAIL"))
        print("Performent: ", metric)

if __name__ == '__main__':
    WorldQuantTool()