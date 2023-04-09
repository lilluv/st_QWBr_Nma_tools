import requests
import json
import csv
from utils import load_params
from urllib.parse import urljoin
from time import sleep
    
class Simulate_API():
    def __init__(self):
        account = load_params()['account']
        self.session = self.login(account)

        self.simulation_data = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": "USA",
                "universe": "TOP3000",
                "delay": 1,
                "decay": 4,
                "neutralization": "NONE",
                "truncation": 0.08,
                "pasteurization": "ON",
                "unitHandling": "VERIFY",
                "nanHandling": "OFF",
                # "selectionLimit": ,
                "language": "FASTEXPR",
                "visualization": False,
            },
            # "regular": "rank(" + str(A[i]) "/" + str(B[j]) + ")",
            "regular": "rank(assets/close)"
            # "combo": ,
            # "selection": ,
        }

    def login(self, account:dict): 
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
    
    def simulate(self, alpha= None):
        #Khoi tao alpha de simulate
        # self.simulation_data.update({"delay": delay}) 
        if alpha:
            self.simulation_data.update({"regular": str(alpha)})
        #Gui request den server
        simulation_response = self.session.post(
            "https://api.worldquantbrain.com/simulations", json=self.simulation_data
        )

        # print("Simulation response: " + str(simulation_response))
        # print(simulation_response.text)

        simulation_progress_url = simulation_response.headers["Location"]
        finished = False

        while True:
            self.simulation_progress = self.session.get(simulation_progress_url)
            if self.simulation_progress.headers.get("Retry-After", 0) == 0:
                break
            # print("Sleeping for " + self.simulation_progress.headers["Retry-After"] + " seconds")
            sleep(float(self.simulation_progress.headers["Retry-After"]))

        # print("--Alpha done simulationg, getting alpha details--")
        metric, success = self.visualize_reponse()
        # print("Performent: ",  metric)
        return metric, success

    def visualize_reponse(self):
        #Lay thong tin alpha    
        # print("simulation_progress.json(): \n",self.simulation_progress.json())
        alpha_id = self.simulation_progress.json().get("alpha")
        # print("\nAlpha: \n", self.simulation_progress.json().get('regular'))

        if self.simulation_progress.json().get('status') != "ERROR":
            alpha = self.session.get("https://api.worldquantbrain.com/alphas/" + alpha_id)

            json_alpha = json.loads(alpha.text)
            # json_alpha_str = json.dumps(json_alpha, indent=2)
            # print(json_alpha_str)
            metric = json_alpha.get('is')
            for is_check in metric['checks']:
                if is_check['result'] == 'FAIL':
                    metric['Test'] = 'FAIL'
                    break
            else:
                metric['Test'] = 'PASS'
            del metric["checks"]
            success = True
        else:
            metric = {}
            success = False
            # print("--ERROR--")
        return metric, success
    
if __name__ == '__main__':
    simAPI = Simulate_API()
    alpha = 'rank(close)'
    simAPI.simulate(alpha)