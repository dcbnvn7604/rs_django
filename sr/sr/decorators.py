from rest_framework.authentication import TokenAuthentication


def graphql_login_required(func):
    def _func(root, info, *args, **kwargs):
        authenticator = TokenAuthentication()
        user_auth_tuple = authenticator.authenticate(info.context)
        if user_auth_tuple is None:
            return None
        return func(root, info, *args, **kwargs)
    return _func


def graphql_permission_required(perm):
    if isinstance(perm, str):
        perms = (perm, )
    else:
        perms = perm
    def _decorator(func):
        def _func(root, info, *args, **kwargs):
            if not user.has_perms(perms):
                return None
            return func(root, info, *args, **kwargs)
        return _func()
    return _decorator
