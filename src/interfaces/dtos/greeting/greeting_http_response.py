from flask import jsonify
from pydantic import BaseModel, ConfigDict


class GreetingHttpResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        # The typed decorator will call this to parse incoming JSON
        return cls.model_validate(data)

    def __call__(self, environ, start_response):
        """Make the class WSGI callable"""
        return jsonify(self.to_dict())(environ, start_response)
