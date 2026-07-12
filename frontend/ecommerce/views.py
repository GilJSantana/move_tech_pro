from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ecommerce.services import BackendClient, BackendClientError
from ecommerce.services.base import BaseBackendClient


def get_backend_client() -> BaseBackendClient:
    return BackendClient(base_url=settings.BACKEND_API_URL)


def index(request: HttpRequest, client: BaseBackendClient | None = None) -> HttpResponse:
    backend_client = client or get_backend_client()

    if request.method == "POST":
        payload = {
            "produto": request.POST.get("produto", "").strip(),
            "quantidade": int(request.POST.get("quantidade", "1") or 1),
        }
        try:
            order = backend_client.criar_pedido(payload)
            order_id = order.get("id") or order.get("order_id") or "N/A"
            messages.success(request, f"Pedido criado com sucesso (ID: {order_id}).")
        except BackendClientError as exc:
            messages.error(request, str(exc))
        return redirect("ecommerce:index")

    try:
        orders = backend_client.listar_pedidos()
        health = backend_client.checar_saude()
    except BackendClientError as exc:
        messages.error(request, str(exc))
        orders = []
        health = {"status": "indisponível"}

    context = {
        "orders": orders,
        "health": health,
        "backend_api_url": settings.BACKEND_API_URL,
    }
    return render(request, "ecommerce/index.html", context)
