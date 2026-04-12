import os
import unittest
from voom_integration_sdk.client import Client
from voom_integration_sdk.units import UnitFactory
import uuid

class TestClientE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We use the previous credentials used for JS/PHP manually
        cls.client_id = os.getenv("VOOM_CLIENT_ID", "test client")
        cls.client_secret = os.getenv("VOOM_CLIENT_SECRET", "test secret")
        
        if cls.client_id == "test client" or cls.client_secret == "test secret":
            cls._skip_e2e = True
        else:
            cls._skip_e2e = False
        
        cls.client = Client(cls.client_id, cls.client_secret)

    def setUp(self):
        if hasattr(self, "_skip_e2e") and self._skip_e2e:
            self.skipTest("Skipping E2E tests: VOOM_CLIENT_ID or VOOM_CLIENT_SECRET not set.")

    def test_01_hello(self):
        try:
            response = self.client.hello()
            self.assertIsNotNone(response)
        except Exception as e:
            self.fail(f"Hello endpoint failed: {e}")

    def test_02_bulk_push(self):
        random_id = str(uuid.uuid4())[:8]
        try:
            unit = UnitFactory.make(
                unit_id=f"E2E-{random_id}",
                tenant_id="T1",
                project_id="P1",
                name="E2E Test Unit",
                unit_type="Apartment",
                code=f"E2E-Code-{random_id}",
                availability="available",
                area=120.5,
                bedrooms=3,
                price=750000.0
            )
            response = self.client.bulk_push([unit])
            self.assertIsNotNone(response)
            # Typically you'd check something in the response, e.g., status 200 or successful parse
        except Exception as e:
            self.fail(f"Bulk push endpoint failed: {e}")

    def test_03_get_units(self):
        try:
            response = self.client.get_units()
            self.assertIsNotNone(response)
        except Exception as e:
            self.fail(f"Get units endpoint failed: {e}")

if __name__ == '__main__':
    unittest.main()
