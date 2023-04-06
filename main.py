from src.crawler_data_fields import CBot
    
if __name__ == '__main__':
    bot = CBot()
    url = "https://platform.worldquantbrain.com/learn/data-and-operators/price-volume-data-for-equity"
    save_path = "Price Volume Data for Equity.csv"
    bot.crawler(url=url, save_path=save_path)