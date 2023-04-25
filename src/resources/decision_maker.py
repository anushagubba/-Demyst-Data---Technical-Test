from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

from server.instance import server

app = server.app
api = server.api

business_info = api.model(
    "Business Info",
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
        "preAssessmentValue": fields.String(20),
    },
)


@api.route("/decisionMaker/")
class DecisionMaker(Resource):
    @api.expect(business_info)
    def post(self):
        req = request.get_json()
        decision = jsonify(
            "Your application has been submitted............ Probable loan amount that could be sanctioned based on the information provided in your application is "
            + str(int(req["preAssessmentValue"]))
            + "% ("
            + str(int(req["LoanAmount"]) * int(req["preAssessmentValue"]) / 100)
            + "). This is not loan sanction confirmation"
        )
        return decision
