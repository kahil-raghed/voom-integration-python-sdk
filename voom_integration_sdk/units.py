from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Unit:
    unit_id: str
    tenant_id: str
    project_id: str
    name: str
    type: str
    code: str
    availability: str
    area: float
    bedrooms: int
    price: float

    def to_dict(self):
        return asdict(self)

class UnitFactory:
    @staticmethod
    def make(unit_id, tenant_id, project_id, name, unit_type, code, availability, area, bedrooms, price, data=None):
        return Unit(
            unit_id=unit_id,
            tenant_id=tenant_id,
            project_id=project_id,
            name=name,
            type=unit_type,
            code=code,
            availability=availability,
            area=float(area),
            bedrooms=int(bedrooms),
            price=float(price)
        )