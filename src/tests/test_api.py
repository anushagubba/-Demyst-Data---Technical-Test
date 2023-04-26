from src.resources.loan_processor import *
from src.resources.decision_maker import *
from src.resources.generate_balance_sheet import *

# from src.conftest import app
import pytest
from server.instance import server

app = server.app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_decision_maker(client):
    payload = {
        "Name": "The Company",
        "LoanAmount": 1000000,
        "YearEstablished": 2020,
        "SummaryOfProfitorLoss": str(
            {
                "Balance Sheet": [
                    {
                        "assetsValue": 4097,
                        "month": 1,
                        "profitOrLoss": -124691,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 9331,
                        "month": 2,
                        "profitOrLoss": 1514,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 20317,
                        "month": 3,
                        "profitOrLoss": 49210,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 470,
                        "month": 4,
                        "profitOrLoss": -186432,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 17522,
                        "month": 5,
                        "profitOrLoss": -31343,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 22857,
                        "month": 6,
                        "profitOrLoss": 5167,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 14740,
                        "month": 7,
                        "profitOrLoss": 68723,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 21661,
                        "month": 8,
                        "profitOrLoss": 100652,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 6960,
                        "month": 9,
                        "profitOrLoss": 94840,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 16927,
                        "month": 10,
                        "profitOrLoss": 231991,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 23189,
                        "month": 11,
                        "profitOrLoss": 138174,
                        "year": 2020,
                    },
                    {
                        "assetsValue": 13,
                        "month": 12,
                        "profitOrLoss": -3498,
                        "year": 2020,
                    },
                ],
                "Total Profit/Loss": 2048409,
                "Average assetsValue": 43209,
            }
        ),
        "preAssessmentValue": 20,
    }
    response = client.post("/decisionMaker/", json=payload)
    assert response.status_code == 200


def test_generate_balance_sheet(client):
    response = client.get("/balSheet/2022/")
    assert response.status_code == 200


def test_loan_inititate(client):
    for rule in app.url_map.iter_rules():
        print(rule)
    response = client.get("/loanInititate/")
    print(response)
    assert response.status_code == 200
    assert response.json == {"message": "Loan Application Process Initiated"}


def test_fetch_bal_sheets_redirection(client):
    response = client.get("/fetchBalSheets/abc/2022")
    assert response.status_code == 308
