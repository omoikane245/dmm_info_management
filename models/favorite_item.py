import dataclasses

@dataclasses.dataclass
class FavoriteItem:
    content_id: str
    site: str
    floor: str
    service: str
    is_bought: bool