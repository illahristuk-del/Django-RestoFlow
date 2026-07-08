from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache


def health_check(request):
    db_ok = False
    redis_ok = False

    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    try:
        cache.set("health_check", "ok", 10)
        redis_ok = cache.get("health_check") == "ok"
    except Exception:
        redis_ok = False

    all_ok = db_ok and redis_ok
    status_code = 200 if all_ok else 503

    return JsonResponse(
        {
            "status": "healthy" if all_ok else "unhealthy",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
        },
        status=status_code,
    )
