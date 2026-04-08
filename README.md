# Voom Integration Python SDK

The **Voom Integration Python SDK** provides a convenient way to interact with the Voom CRM Integration API. It simplifies authentication and provides a structured way to push inventory units and manage data.

## Features

- **Automated Signature Generation**: Handles HMAC-SHA256 signing for secure API requests.
- **Easy Unit Management**: Includes a `UnitFactory` to create standardized inventory units.
- **Support for Multiple Auth Modes**: Supports both Signature-based and Basic authentication.
- **Robust Client**: Built on top of the `requests` library for reliability.

## Installation

You can install the Voom Integration SDK using pip:

```bash
pip install voom-integration-sdk
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/kahil-raghed/voom-integration-python-sdk.git
cd voom-integration-python-sdk
pip install .
```

## Dependencies

- Python >= 3.7
- requests >= 2.25.0

## Quick Start

### 1. Initialize the Client

To get started, you need your `client_id` and `client_secret` provided by Voom.

```python
from voom_integration_sdk.client import Client

client_id = "your_client_id"
client_secret = "your_client_secret"

client = Client(client_id, client_secret)
```

### 2. Test Connection

Use the `hello()` method to verify your credentials and connection.

```python
try:
    response = client.hello()
    print("Connection Successful:", response)
except Exception as e:
    print("Connection Failed:", e)
```

### 3. Push Inventory Units

Use the `UnitFactory` to create units and push them in bulk.

```python
from voom_integration_sdk.units import UnitFactory

# Create a unit
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

# Push the unit
response = client.bulk_push([unit])
print("Push Response:", response)
```

## Authentication

The SDK defaults to **Signature-based Authentication**, which uses HMAC-SHA256 to sign each request. This is the most secure method as it prevents replay attacks and ensures data integrity.

Each request includes:
- `X-Client-Id`: Your Client ID.
- `X-Request-Id`: A unique UUID for each request.
- `X-Request-Time`: ISO 8601 timestamp.
- `X-Request-Signature`: HMAC signature.

### Basic Authentication (Optional)

If your environment requires Basic Auth, you can enable it:

```python
client = Client(client_id, client_secret, basic_auth=("username", "password"))
client.use_basic_auth(True)
```

## API Reference

### `Client`

- `__init__(client_id, client_secret, basic_auth=None)`: Initialize the client.
- `hello()`: Verifies connection and credentials.
- `bulk_push(units)`: Sends a list of units to the Voom CRM.
- `get_units()`: Retrieves units from the CRM (default pagination: page 1, 10 items).
- `use_basic_auth(enable)`: Toggles Basic Authentication mode.

### `UnitFactory`

- `make(...)`: Helper method to create a `Unit` object with all required fields.

## Running Tests

The SDK uses `unittest` for testing. You can run the end-to-end tests using the following command:

```bash
export VOOM_CLIENT_ID="your_client_id"
export VOOM_CLIENT_SECRET="your_client_secret"
python -m unittest discover tests
```

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please contact the development team at Voom.
