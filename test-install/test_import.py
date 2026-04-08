import sys
import os

try:
    from voom_integration_sdk.client import Client
    from voom_integration_sdk.units import UnitFactory
    
    print("Successfully imported Client and UnitFactory!")
    
    # Simple check of UnitFactory
    unit = UnitFactory.make(
        unit_id="TEST-1",
        tenant_id="T1",
        project_id="P1",
        name="Test Unit",
        unit_type="Studio",
        code="T-01",
        availability="available",
        area=50.0,
        bedrooms=1,
        price=100000.0
    )
    print(f"Successfully created a test unit: {unit.name}")
    
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
