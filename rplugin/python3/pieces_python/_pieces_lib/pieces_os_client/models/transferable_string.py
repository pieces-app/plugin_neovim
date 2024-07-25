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


from typing import Optional
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictStr
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class TransferableString(BaseModel):
    """
    This is a String representaion of any of these changes.  [NOT IMPLEMENTED] base64, base64_url, data_url [IMPLEMENTED] raw  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    raw: Optional[StrictStr] = Field(default=None, description="IMPLEMENTED")
    var_base64: Optional[StrictStr] = Field(default=None, alias="base64", description="NOT IMPLEMENTED")
    base64_url: Optional[StrictStr] = Field(default=None, description="NOT IMPLEMENTED")
    data_url: Optional[StrictStr] = Field(default=None, description="NOT IMPLEMENTED")
    __properties = ["schema", "raw", "base64", "base64_url", "data_url"]

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
    def from_json(cls, json_str: str) -> TransferableString:
        """Create an instance of TransferableString from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransferableString:
        """Create an instance of TransferableString from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransferableString.parse_obj(obj)

        _obj = TransferableString.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "raw": obj.get("raw"),
            "var_base64": obj.get("base64"),
            "base64_url": obj.get("base64_url"),
            "data_url": obj.get("data_url")
        })
        return _obj


