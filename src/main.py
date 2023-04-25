from server.instance import server

# Need to import all resources
from resources.generate_balance_sheet import *
from resources.decision_maker import *
from resources.loan_processor import *


if __name__ == "__main__":
    server.run()
