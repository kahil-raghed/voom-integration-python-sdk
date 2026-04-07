import hmac
import hashlib
import base64
import uuid
import requests
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

class VoomClient:
    DEFAULT_BASE_URL = "https://crm-integration.voomproject.com"
    
    API_HELLO = "/api/client-api/v1/hello"
    API_BULK_PUSH = "/api/client-api/v1/inventory/bulk-push"
    API_GET_UNITS = "/api/client-api/v1/inventory/get-units"

    def __init__(self, client_id: str, client_secret: str, basic_auth: Optional[tuple] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.basic_auth = basic_auth
        self.base_url = self.DEFAULT_BASE_URL
        self.is_basic_auth_enabled = False

    def use_basic_auth(self, enable: bool = True):
        if enable and not self.basic_auth:
            raise ValueError("Basic Auth credentials must be provided in the constructor.")
        self.is_basic_auth_enabled = enable

    def _generate_signature(self, request_id: str, request_time: str) -> str:
        # Sign: client_id + request_id + request_time
        string_to_sign = f"{self.client_id}{request_id}{request_time}"
        
        signature = hmac.new(
            self.client_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')

    def _call_api(self, method: str, path: str, data: Optional[Dict] = None):
        url = f"{self.base_url}{path}"
        headers = {'Content-Type': 'application/json'}
        auth = None

        if self.is_basic_auth_enabled:
            auth = self.basic_auth
        else:
            request_id = str(uuid.uuid4())
            request_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            signature = self._generate_signature(request_id, request_time)

            headers.update({
                'X-Client-Id': self.client_id,
                'X-Request-Id': request_id,
                'X-Request-Time': request_time,
                'X-Request-Signature': signature
            })

        response = requests.request(method, url, json=data, headers=headers, auth=auth)
        response.raise_for_status()
        return response.json()

    def hello(self):
        return self._call_api("POST", self.API_HELLO)

    def bulk_push(self, units: List[Any]): # Using Any to avoid circular import in simple example
        data = {"units": [u.to_dict() if hasattr(u, "to_dict") else u for u in units]}
        return self._call_api("POST", self.API_BULK_PUSH, data)

    def get_units(self):
        return self._call_api("GET", self.API_GET_UNITS)