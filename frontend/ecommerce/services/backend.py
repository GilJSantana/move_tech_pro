from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from .base import BaseBackendClient


@dataclass
class BackendClientError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class BackendClient(BaseBackendClient):
    def __init__(self, base_url: str, timeout: float = 5.0, session: requests.Session | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = session or requests.Session()

    def criar_pedido(self, payload: dict) -> dict:
        response = self._request("POST", "/orders", json=payload)
        return self._json_or_empty_dict(response)

    def listar_pedidos(self) -> list:
        response = self._request("GET", "/orders")
        data = self._json_or_empty(response)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("orders"), list):
            return data["orders"]
        return []

    def checar_saude(self) -> dict:
        response = self._request("GET", "/health")
        data = self._json_or_empty(response)
        return data if isinstance(data, dict) else {"status": "unknown"}

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.request(method=method, url=url, timeout=self._timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.Timeout as exc:
            raise BackendClientError("Timeout ao comunicar com a API de backend.") from exc
        except requests.ConnectionError as exc:
            raise BackendClientError("Falha de conexão com a API de backend.") from exc
        except requests.HTTPError as exc:
            status_code = getattr(exc.response, "status_code", "desconhecido")
            raise BackendClientError(f"Erro HTTP da API de backend (status: {status_code}).") from exc
        except requests.RequestException as exc:
            raise BackendClientError("Erro inesperado na comunicação com a API de backend.") from exc

    @staticmethod
    def _json_or_empty(response: requests.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return {}

    @classmethod
    def _json_or_empty_dict(cls, response: requests.Response) -> dict:
        data = cls._json_or_empty(response)
        return data if isinstance(data, dict) else {}
