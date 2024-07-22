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


from typing import Optional, Union
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictFloat, StrictInt
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from pieces_python._pieces_lib.pieces_os_client.models.updating_status_enum import UpdatingStatusEnum

class OSServerUpdateStatus(BaseModel):
    """
    This is the model for the progress of the current update of Pieces os.  /os/update/check/stream && /os/update/check/  we will emit on a progress update  updated: is an optional property that will let us know when the update was checked last.  NOTE: it is reccommended to use the stream instead of pulling. NOTE: lets think about if we want to have a closing(as well as how we want to handle restarts)  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    status: UpdatingStatusEnum = Field(...)
    updated: Optional[GroupedTimestamp] = None
    percentage: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Optionally if the update is in progress you will recieve a download percent(from 0-100).")
    __properties = ["schema", "status", "updated", "percentage"]

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
    def from_json(cls, json_str: str) -> OSServerUpdateStatus:
        """Create an instance of OSServerUpdateStatus from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # set to None if percentage (nullable) is None
        # and __fields_set__ contains the field
        if self.percentage is None and "percentage" in self.__fields_set__:
            _dict['percentage'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OSServerUpdateStatus:
        """Create an instance of OSServerUpdateStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OSServerUpdateStatus.parse_obj(obj)

        _obj = OSServerUpdateStatus.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "status": obj.get("status"),
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "percentage": obj.get("percentage")
        })
        return _obj


