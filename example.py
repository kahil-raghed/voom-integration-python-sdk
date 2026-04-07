import os
from src.client import VoomClient
from src.units import UnitFactory

# 1. Initialize the client
# Replace with your actual credentials or use environment variables
client_id = os.getenv("VOOM_CLIENT_ID", "your_client_id")
client_secret = os.getenv("VOOM_CLIENT_SECRET", "your_client_secret")

client = VoomClient(client_id, client_secret)

# 2. Test connection (Hello endpoint)
try:
    print("Testing 'Hello' endpoint...")
    hello_response = client.hello()
    print("Hello Response:", hello_response)
    
    # 3. Try to push a test unit
    unit = UnitFactory.make(
        unit_id="U101",
        tenant_id="T1",
        project_id="P1",
        name="Penthouse Suite",
        unit_type="Apartment",
        code="PH-01",
        availability="available",
        area=120.5,
        bedrooms=3,
        price=750000.0
    )
    
    print("\nPushing a test unit...")
    push_response = client.bulk_push([unit])
    print("Push Response:", push_response)

except Exception as e:
    print(f"An error occurred: {e}")
