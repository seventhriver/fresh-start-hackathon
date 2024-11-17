from flask import Flask, request
import routes.oauth.exchangeToken
from routes.banks.bankRoutes import (
    get_all_drivers,
    get_all_orders,
    assign_order_to_driver,
    create_bank_order,
)
from routes.banks.getOrders import getOrders
from routes.providers.createProvider import createProvider
from routes.providers.createOrder import createOrder
from routes.drivers.createDriver import createDriver
from routes.banks.createBank import createBank
from routes.getUserType import getUserType
import logging

# from routes.providers.createOrder import createOrder
from flask_cors import CORS


def main(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    CORS(app)
    app.config.from_mapping(
        # SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    @app.route("/")
    def hello():
        return "ok"

    @app.route("/api/v1/providers/get_user", methods=["POST"])
    def get_providers():
        # return getUser(request.json)
        return ""

    @app.route("/api/v1/providers/create_provider", methods=["POST"])
    def create_providers():
        return createProvider(request.json)

    @app.route("/api/v1/drivers/create_driver", methods=["POST"])
    def create_drivers():
        return createDriver(request.json)

    @app.route("/api/v1/providers/banks/create_bank", methods=["POST"])
    def create_banks():
        return createBank(request.json)

    @app.route("/api/v1/oauth/exchange_token", methods=["POST"])
    def exchange_token():
        return routes.oauth.exchangeToken.handle_google_auth(request.json)

    @app.route("/api/v1/providers/create_order", methods=["POST"])
    def create_order():
        return createOrder(request.json)

    @app.route("/api/v1/drivers/get_orders", methods=["POST"])
    def get_orders():
        return getOrders(request.json)

    @app.route("/api/v1/banks/get_all_drivers", methods=["POST"])
    def bank_get_drivers():
        return get_all_drivers(request.json)

    @app.route("/api/v1/banks/get_all_orders", methods=["POST"])
    def bank_get_orders():
        return get_all_orders(request.json)

    @app.route("/api/v1/banks/assign_order", methods=["POST"])
    def bank_assign_order():
        return assign_order_to_driver(request.json)

    @app.route("/api/v1/get_user_type", methods=["POST"])
    def get_user_type():
        return getUserType(request.json)

    return app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
