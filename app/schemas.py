
from pydantic import BaseModel, Field


class ListingInput(BaseModel):
    neighbourhood_group: str
    neighbourhood: str

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    room_type: str

    minimum_nights: int = Field(ge=1)
    number_of_reviews: int = Field(ge=0)
    reviews_per_month: float | None = Field(default=None, ge=0)
    calculated_host_listings_count: int = Field(ge=1)
    availability_365: int = Field(ge=0, le=365)


class PredictionOutput(BaseModel):
    predicted_price: float
    currency: str = "USD"
