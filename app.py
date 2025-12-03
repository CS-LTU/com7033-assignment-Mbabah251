
from flask import Flask, render_template
import os
from routes.auth import auth_routes
from routes.patient import patient_routes
from schema.users import users_schema
from schema.patients import patients_schema



app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

auth_routes(app)
patient_routes(app)

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
