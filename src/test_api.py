import requests
import json
import csv
from utils import load_params
from urllib.parse import urljoin
from time import sleep
import logging
from datetime import datetime

logging.basicConfig(filename="API_Response.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
    
class Simulate_API():
    def __init__(self):
        params = load_params()
        account = params['account']
        self.session = self.login(account)
        self.simulation_data = params['config']
        logger.info("Start Simulator API: ", datetime.now())

    def login(self, account:dict): 
        """Log in Script 

        Args:
            account (dict): Contain login information
                - user_name: User name
                - pwd: Password
        Returns:
            s: session
        """        
        s = requests.Session() #Tao request
        s.auth = (account['user_name'], account['pwd'])
        #Login
        response = s.post("https://api.worldquantbrain.com/authentication")
        print("Response Login:" + str(response))
        # print(response.text)
        if response.status_code == requests.status_codes.codes.unauthorized:
            if response.headers["WWW-Authenticate"] == "persona":
                input(
                    "Complete biometrics authentication and press any key to continue: "
                    + urljoin(response.url, response.headers["Location"])
                )
                s.post(urljoin(response.url, response.headers["Location"]))
            else:
                print("incorrect email and password")
        return s
    
    def simulate(self, alpha: str=None):     
        """Simulate Alpha to get Performent

        Args:
            alpha (str, optional): Alpha. Defaults to None.

        Returns:
            tuple: 
                - metric (dict): perform metric (sharpe, longcount, ...)
                - success (bool): Accept Request
        """        
        #Khoi tao alpha de simulate
        if alpha:
            self.simulation_data.update({"regular": str(alpha)})
        #Gui request den server
        simulation_response = self.session.post(
            "https://api.worldquantbrain.com/simulations", json=self.simulation_data
        )

        simulation_progress_url = simulation_response.headers.get("Location")
        if simulation_progress_url:
            while True:
                self.simulation_progress = self.session.get(simulation_progress_url)
                if self.simulation_progress.headers.get("Retry-After", 0) == 0:
                    break
                sleep(float(self.simulation_progress.headers["Retry-After"]))
            # print("--Alpha done simulationg, getting alpha details--")
            metric, success = self.visualize_reponse()
            return metric, success
        else:
            logger.warning("Simulation Response cant get \"Location\": ", alpha)
            return {}, False

    def visualize_reponse(self):
        #Lay thong tin alpha    
        alpha_id = self.simulation_progress.json().get("alpha")
        metric = {}
        if alpha_id is None:
            logger.error("--Simulate ERROR--\n"+ self.simulation_progress.json().get('message'))
            return metric, False
        if self.simulation_progress.json().get('status') != "ERROR":
            alpha = self.session.get("https://api.worldquantbrain.com/alphas/" + alpha_id)
            json_alpha = json.loads(alpha.text)
            metric = json_alpha.get('is')
            for is_check in metric['checks']:
                if is_check['result'] == 'FAIL':
                    metric['Test'] = 'FAIL'
                    break
            else:
                metric['Test'] = 'PASS'
            del metric["checks"]
            return metric, True
        else:
            # print("--ERROR--")
            logger.error("--Simulate ERROR--\n", self.simulation_progress.json().get('message'))
            return metric, False
    
if __name__ == '__main__':
    simAPI = Simulate_API()
    alpha = 'rank(close)'
    simAPI.simulate(alpha)