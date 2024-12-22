from flask import Flask
from app.routes.analyze_routes import analyze_attacks_blueprint





app = Flask(__name__)


app.register_blueprint(analyze_attacks_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)