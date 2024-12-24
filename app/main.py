from flask import Flask
from app.routes.analyze_routes import analyze_attacks_blueprint
from flask_cors import CORS
from app.routes.search_routes import search_keywords_blueprint



app = Flask(__name__)

CORS(app)


app.register_blueprint(analyze_attacks_blueprint, url_prefix='/api')
app.register_blueprint(search_keywords_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)