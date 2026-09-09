from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return {'message': 'Phase 2 API is running'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
