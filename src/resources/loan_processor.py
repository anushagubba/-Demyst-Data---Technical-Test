from flask import Flask, request, jsonify
import requests, ast, json
from flask_restx import Api, Resource, fields

from server.instance import server

app = server.app
api = server.api

application_info = api.model(
    "Application Info",
    {
        "Name": fields.String("The Company"),
        "LoanAmount": fields.String(1000000),
        "YearEstablished": fields.String(2022),
        "SummaryOfProfitorLoss": fields.String(
            str(
                {
                    "bal_sheet": [
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
            )
        ),
    },
)


@api.route("/loanInititate/")
class LoanInitiate(Resource):
    def get(self):
        response = jsonify(message="Loan Application Process Initiated")
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@api.route("/fetchBalSheets/<string:provider>/<int:est_year>/")
class FetchBalSheets(Resource):
    def get(self, provider, est_year):
        PL = AV = 0
        bal_sheet = ast.literal_eval(
            requests.get(
                url="http://127.0.0.1:5000/balSheet/" + str(est_year) + "/"
            ).text
        )
        for item in bal_sheet:
            PL += int(item.get("profitOrLoss"))
            AV += int(item.get("assetsValue"))
        response =  jsonify({
            "bal_sheet": bal_sheet,
            "Total Profit/Loss": PL,
            "Average assetsValue": round(AV / 12, 2),
        })
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@api.route("/submit/")
class SubmitApplication(Resource):
    @api.expect(application_info)
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            req = request.get_json()
            preAssessment = 20
            loan_amount = int(req["LoanAmount"])
            AAV = int(
                ast.literal_eval(req["SummaryOfProfitorLoss"])[
                    "Average assetsValue"
                ]
            )
            PL = int(
                ast.literal_eval(req["SummaryOfProfitorLoss"])[
                    "Total Profit/Loss"
                ]
            )
            if PL > 0:
                preAssessment = 60
                if AAV > loan_amount:
                    preAssessment = 100
            req.update({"preAssessmentValue": str(preAssessment)})
            decision_maker_result = requests.post(url="http://127.0.0.1:5000/decisionMaker/", json=req)
            decision = jsonify(message=decision_maker_result.text.replace('"',''))
            # decision.headers.add('Access-Control-Allow-Origin','*')
            # decision.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
            # decision.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE')
            # decision.headers["Access-Control-Allow-Headers"] = \
            # "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, " + \
            # "X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
            return decision
        else:
            return 'Content-Type not supported!'
        