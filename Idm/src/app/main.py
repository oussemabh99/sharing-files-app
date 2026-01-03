from app.routes.idm import auth_bp
from app.routes.auth import idm_bp
from app.routes.tenant import tenant_bp
def register_routes(app):
    app.register_blueprint(idm_bp, url_prefix="/auth/api/v1/")
    app.register_blueprint(auth_bp, url_prefix="/idm/api/v1/")
    app.register_blueprint(tenant_bp, url_prefix="/tenant/api/v1/<org>")
    
    
