from flask import Flask, render_template, session
import os
from routes.auth import auth_routes
from routes.users import users_routes
from routes.patient import patient_routes
from schema.users import users_schema
from schema.patients import patients_schema
from utils.users_utils import get_current_user



app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

@app.context_processor
def inject_current_user():
    """Make current logged-in user available in all templates"""
    current_user = None
    if 'user_id' in session:
        current_user = get_current_user()
    return dict(current_user=current_user)

auth_routes(app)
patient_routes(app)
users_routes(app)

users_schema()
patients_schema()


@app.errorhandler(404)
def not_found(e):
    """
    Handle 404 errors (page not found)
    Returns custom 404 template
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    """
    Handle 500 errors (internal server errors)
    Returns custom error template
    """
    return render_template("404.html"), 500


if __name__ == "__main__":
    app.run(debug=True)