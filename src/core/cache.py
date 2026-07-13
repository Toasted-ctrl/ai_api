from fastapi import Request, Response
from fastapi_cache import FastAPICache

def cache_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    
    """Build cache key to store results including the email id of the user.
    Requires request: Request to be included in the main function call."""

    user_email = request.headers.get("X-User-Email", "anonymous")
    prefix = FastAPICache.get_prefix()
    return f"{prefix}:{func.__name__}:{user_email}"