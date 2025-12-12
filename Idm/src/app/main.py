from flask import Blueprint

from app.routes.auth import auth_bp

def register_routes(app):

    app.register_blueprint(auth_bp, url_prefix="/idm/api/v1/")
    
