from flask import Flask
from api.routes import bp
from pki.ca import bootstrap_ca
import config

def create_app():
    app = Flask(__name__)
    
    # Create storage folders if they don't exist
    import os, config
    for folder in config.STORAGE.values():
        os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.dirname(config.CA_CERT_PATH), exist_ok=True)
    
    bootstrap_ca()
    app.register_blueprint(bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=5000)