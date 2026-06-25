from flask import Flask
from api.routes import bp
from pki.ca import bootstrap_ca
import config

def create_app():
    app = Flask(__name__)
    bootstrap_ca()          # ensures CA exists on startup
    app.register_blueprint(bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=5000)