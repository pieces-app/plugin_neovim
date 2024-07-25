# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json



from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictStr

class Auth0UserAllocationMetadata(BaseModel):
    """
    This is specifically for our allocation server metadata.  # noqa: E501
    """
    project: StrictStr = Field(...)
    region: StrictStr = Field(...)
    __properties = ["project", "region"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Auth0UserAllocationMetadata:
        """Create an instance of Auth0UserAllocationMetadata from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Auth0UserAllocationMetadata:
        """Create an instance of Auth0UserAllocationMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Auth0UserAllocationMetadata.parse_obj(obj)

        _obj = Auth0UserAllocationMetadata.parse_obj({
            "project": obj.get("project"),
            "region": obj.get("region")
        })
        return _obj


