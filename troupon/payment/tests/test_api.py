"""Tests for transactions API endpoints."""
from rest_framework.test import APITestCase


class TransactionAPITest(APITestCase):
    """Tests for transaction api endpoints."""

    fixtures = ['purchases.json']

    def test_list_transactions(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_list_one_transaction(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.get('/api/transactions/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_delete_one_transaction(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.delete('/api/transactions/2')
        self.assertEqual(response.status_code, 204)

    def test_unauthorized_list_transactions(self):
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 403)
