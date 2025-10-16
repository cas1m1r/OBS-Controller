from flask import request, abort
from .config import cfg

ROLE_TOKENS = {
    'admin': lambda: cfg('ADMIN_TOKEN',''),
    'producer': lambda: cfg('PRODUCER_TOKEN','')
}

def resolve_role(token: str):
    for role, getter in ROLE_TOKENS.items():
        if token and token == getter():
            return role
    return None

def require_role(allowed_roles):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            token = request.headers.get('X-Auth-Token') or request.args.get('token')
            role = resolve_role(token)
            if role is None or role not in allowed_roles:
                abort(401)
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator