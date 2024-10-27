import dataclasses

@dataclasses.dataclass
class Item:
    content_id: str
    title: str
    affiliate_url: str
    sample_image_url: str
    price: str
    is_sale: bool
