import random
from .test_api import Simulate_API
from utils import load_params
import pandas as pd
from itertools import combinations
# from itertools import permutations
from tqdm import tqdm 
import csv

class Alpha_Generator():
    def __init__(self):
        self.params = load_params()
        self.simAPI = Simulate_API()

    def combine_alpha(self, list_alpha, field_neutralization = 'industry'):
        # random_weight = random.sample(range(1, 10), len(list_alpha))
        # w_alpha = [x/sum(random_weight) for x in random_weight ]
        # w_alpha = random_weight
        
        list_processed_alpha = []
        for idx, alpha in enumerate(list_alpha):
            if field_neutralization:
                alpha = "scale(group_neutralize({0}, {1}))".format(alpha, field_neutralization)
            else:
                alpha = "scale({0})".format(alpha)
            list_processed_alpha.append(alpha)
        f_alpha = ','.join(list_processed_alpha)

        return "add({0})".format(f_alpha)

    def generate(self, formula = "{0}+{1}", num_variable=2, dataset = "price_volume"):
        # Read Data Fields
        data_config = self.params.get("dataset")
        dfs = pd.read_excel(data_config["path"], sheet_name=data_config[dataset])
        List_field_delay0 = []
        List_field_delay1 = []
        for field, delay in zip(dfs['Field'], dfs['Delay']):
            if delay == 0:
                List_field_delay0.append(field)
            else:
                List_field_delay1.append(field)
        Keys = ['Alpha', 'PnL', 'longCount', 'shortCount', 'turnover', 'Returns', 'Drawdown', 'Margin', 'Fitness', 'Sharpe', 'Test']
        # list_variable = list(combinations(List_field_delay0, num_variable))
        with open('test.csv', 'w') as output_file:
            dict_writer = csv.writer(output_file)
            dict_writer.writerow(Keys)
            # list_Permutations = list(permutations(List_field_delay0, num_variable)) #List_field_delay1
            list_Permutations = list(combinations([*List_field_delay0,*List_field_delay1], num_variable))
            for permutation in tqdm(list_Permutations):
                alpha = formula.format(*permutation)
                response, success = self.simAPI.simulate(alpha)
                if success:
                    data_list = [alpha, response.get('pnl'), response.get('longCount'), response.get('shortCount'), response.get('turnover'), response.get('returns'), response.get('drawdown'), response.get('margin'), response.get('fitness'), response.get('sharpe'), response.get('Test')]
                    dict_writer.writerow(data_list)
