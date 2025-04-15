
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    role = getattr(user.profile, 'role', None) if hasattr(user, 'profile') else None

    refresh['username'] = user.username
    refresh['role'] = role

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

