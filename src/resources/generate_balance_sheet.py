import random
from flask import Flask, jsonify
from flask_restx import Api, Resource

from server.instance import server

app = server.app
api = server.api


def generate_bal_sheet(year):
    balance_sheet = []
    for month in range(1, 13):
        balance_sheet.append(
            {
                "year": year,
                "month": month,
                "profitOrLoss": random.randint(-250000, 350000),
                "assetsValue": random.randint(-0, 250000),
            }
        )
    return balance_sheet


@api.route("/balSheet/<int:year>/")
class BalSheet(Resource):
    def get(self, year):
        return jsonify(generate_bal_sheet(year))
