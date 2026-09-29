from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class HomeItem(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    quantity: int = Field(default=1, ge=1, le=50)
    notes: str = Field(default="", max_length=300)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1, max_length=10)
    style: str = Field(default="modern", max_length=80)
    items: list[HomeItem] = Field(default_factory=list, max_length=40)
    city: str = Field(default="India", max_length=100)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=1, max_length=80)
    venue: str = Field(default="", max_length=200)
    city: str = Field(default="India", max_length=100)
    preferences: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=1, max_length=100)
    style: str = Field(default="elegant", max_length=100)
    outfit_description: str = Field(default="", max_length=1000)
    city: str = Field(default="India", max_length=100)
