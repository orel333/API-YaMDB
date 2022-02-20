import jwt

from api_yamdb.settings import SECRET_KEY

def get_user_role(token):
    """Извлекает роль из токена, без обращения к базе."""
    data = jwt.decode(
        jwt=str(token),
        key=SECRET_KEY,
        algorithms=['HS256']
    )
    role = data['role']
    return role