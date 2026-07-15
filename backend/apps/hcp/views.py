"""
HCP module views – scaffold only.
"""
from django.http import JsonResponse


def health_check(request):
    """Simple liveness probe."""
    return JsonResponse({"status": "ok", "module": "hcp"})
