from pydantic import BaseModel, ConfigDict


class PersonName(BaseModel):
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
