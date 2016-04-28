
def ensure_token_match(token, check_methods=None):
    if check_methods is None:
        check_methods = ["list", "create"] + ["retrieve", "update", "destroy"]

    def check(request, view):
        if view.requested_method in check_methods:
            return request.META.get("HTTP_X_KEL_TOKEN", "") == token
    return check


def ensure_user_belongs(attr, check_methods=None):
    if check_methods is None:
        check_methods = ["list", "create"] + ["retrieve", "update", "destroy"]

    def check(request, view):
        if view.requested_method in check_methods:
            return request.user in getattr(view, attr).members()
    return check
