from abc import ABC, abstractmethod


class BaseBackendClient(ABC):
    @abstractmethod
    def criar_pedido(self, payload: dict) -> dict:
        """Dispara um POST para /orders mapeando o contrato da API de referência."""

    @abstractmethod
    def listar_pedidos(self) -> list:
        """Dispara um GET para /orders para exibir no painel."""

    @abstractmethod
    def checar_saude(self) -> dict:
        """Dispara um GET para /health para validar a conectividade do ecossistema."""
