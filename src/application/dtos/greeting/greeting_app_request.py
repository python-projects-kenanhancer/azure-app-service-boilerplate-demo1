from pydantic import BaseModel, ConfigDict


class GreetingAppRequest(BaseModel):
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        # The typed decorator will call this to parse incoming JSON
        return cls.model_validate(data)
