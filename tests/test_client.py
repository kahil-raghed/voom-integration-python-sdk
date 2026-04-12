import unittest
from unittest.mock import patch, MagicMock
from voom_integration_sdk.client import Client
from voom_integration_sdk.units import UnitFactory

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client_id = "test_id"
        self.client_secret = "test_secret"
        self.client = Client(self.client_id, self.client_secret)

    @patch('voom_integration_sdk.client.requests.request')
    def test_hello_success(self, mock_request):
        # Mocking successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Hello World"}
        mock_request.return_value = mock_response

        response = self.client.hello()
        
        self.assertEqual(response, {"message": "Hello World"})
        mock_request.assert_called_once()
        # Verify that the correct URL and method were used
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/client-api/v1/hello", args[1])

    @patch('voom_integration_sdk.client.requests.request')
    def test_bulk_push_success(self, mock_request):
        # Mocking successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response

        unit = UnitFactory.make(
            unit_id="U1", tenant_id="T1", project_id="P1", name="Test Unit",
            unit_type="Type A", code="C1", availability="available",
            area=100.0, bedrooms=2, price=500000.0
        )

        response = self.client.bulk_push([unit])
        
        self.assertEqual(response, {"status": "success"})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/client-api/v1/inventory/bulk-push", args[1])
        
        # Check that payload contains units
        payload = kwargs['json']
        self.assertIn('units', payload)
        self.assertEqual(len(payload['units']), 1)
        self.assertEqual(payload['units'][0]['unit_id'], "U1")

    @patch('voom_integration_sdk.client.requests.request')
    def test_get_units_success(self, mock_request):
        # Mocking successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"units": []}
        mock_request.return_value = mock_response

        response = self.client.get_units()
        
        self.assertEqual(response, {"units": []})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("/api/client-api/v1/inventory/get-units", args[1])

    def test_signature_generation(self):
        # Test HMAC signature generation
        request_id = "test-req-id"
        request_time = "2024-01-01T00:00:00Z"
        
        signature = self.client._generate_signature(request_id, request_time)
        
        # Verify signature is not empty and is a valid base64
        self.assertTrue(len(signature) > 0)
        # Re-generating should give the same signature
        signature2 = self.client._generate_signature(request_id, request_time)
        self.assertEqual(signature, signature2)

if __name__ == '__main__':
    unittest.main()
