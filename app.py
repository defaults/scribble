from flask import Flask

# blueprints
from auth import auth
from api import api
from admin import admin
from blog import blog

# initialise app
app = Flask(__name__)

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(blog)


# warmp reguests
@app.route('/_ah/warmup')
def warmup():
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=9000, debug=True)
