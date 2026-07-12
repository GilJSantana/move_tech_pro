from unittest import TestCase
from unittest.mock import Mock

import requests

from ecommerce.services.backend import BackendClient, BackendClientError


class BackendClientTests(TestCase):
    def setUp(self) -> None:
        self.session = Mock(spec=requests.Session)
        self.client = BackendClient(base_url="http://backend:8000", session=self.session)

    def test_criar_pedido_deve_retornar_payload_quando_sucesso(self) -> None:
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"id": 123}
        self.session.request.return_value = response

        result = self.client.criar_pedido({"produto": "mouse", "quantidade": 1})

        self.assertEqual(result["id"], 123)
        self.session.request.assert_called_once()

    def test_listar_pedidos_deve_lancar_erro_quando_http_500(self) -> None:
        response = Mock()
        response.status_code = 500
        http_error = requests.HTTPError(response=response)
        response.raise_for_status.side_effect = http_error
        self.session.request.return_value = response

        with self.assertRaises(BackendClientError):
            self.client.listar_pedidos()

    def test_checar_saude_deve_lancar_erro_quando_timeout(self) -> None:
        self.session.request.side_effect = requests.Timeout()

        with self.assertRaises(BackendClientError):
            self.client.checar_saude()
