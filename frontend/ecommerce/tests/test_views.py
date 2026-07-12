from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from django.urls import reverse

from ecommerce.services.backend import BackendClientError


class EcommerceViewTests(SimpleTestCase):
    @patch("ecommerce.views.get_backend_client")
    def test_get_index_retorna_200(self, mock_get_client: Mock) -> None:
        client_mock = Mock()
        client_mock.listar_pedidos.return_value = []
        client_mock.checar_saude.return_value = {"status": "ok"}
        mock_get_client.return_value = client_mock

        response = self.client.get(reverse("ecommerce:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ecommerce/index.html")

    @patch("ecommerce.views.get_backend_client")
    def test_post_index_exibe_mensagem_sucesso(self, mock_get_client: Mock) -> None:
        client_mock = Mock()
        client_mock.criar_pedido.return_value = {"id": 999}
        client_mock.listar_pedidos.return_value = []
        client_mock.checar_saude.return_value = {"status": "ok"}
        mock_get_client.return_value = client_mock

        response = self.client.post(
            reverse("ecommerce:index"),
            data={"produto": "teclado", "quantidade": "2"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pedido criado com sucesso")

    @patch("ecommerce.views.get_backend_client")
    def test_post_index_exibe_mensagem_erro(self, mock_get_client: Mock) -> None:
        client_mock = Mock()
        client_mock.criar_pedido.side_effect = BackendClientError("Falha no backend.")
        client_mock.listar_pedidos.return_value = []
        client_mock.checar_saude.return_value = {"status": "ok"}
        mock_get_client.return_value = client_mock

        response = self.client.post(
            reverse("ecommerce:index"),
            data={"produto": "monitor", "quantidade": "1"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Falha no backend.")
