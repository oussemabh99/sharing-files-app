from app.routes.idm import auth_bp
from app.routes.auth import idm_bp
def register_routes(app):
    app.register_blueprint(idm_bp, url_prefix="/auth/api/v1/")
    app.register_blueprint(auth_bp, url_prefix="/idm/api/v1/")
    
    
