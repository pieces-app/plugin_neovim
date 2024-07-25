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
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.external_provider_profile_data import ExternalProviderProfileData
from pieces_python._pieces_lib.pieces_os_client.models.external_provider_type_enum import ExternalProviderTypeEnum
from pieces_python._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp

class ExternalProvider(BaseModel):
    """
    I know that profileData and user_id have differeing casing but they are done because they map to Auth0's projeecties.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    type: ExternalProviderTypeEnum = Field(...)
    user_id: StrictStr = Field(default=..., description="This is the user_id within the provider.")
    access_token: Optional[StrictStr] = Field(default=None, description="This is optional here, but will be present for BB, Github, and google.")
    expires_in: Optional[StrictInt] = Field(default=None, description="Some providers have an expiration on their access token. IE BB, Google, NOT Github.")
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    profile_data: Optional[ExternalProviderProfileData] = Field(default=None, alias="profileData")
    connection: Optional[StrictStr] = Field(default=None, description="This is an optional field that will be provided onentreprise connections. ie is type == waad then connection might be PiecesApp. However is other cases,you my find your provider and connection is the exact same string. To decifer between the two, you can use the isSocial bool.")
    is_social: Optional[StrictBool] = Field(default=None, alias="isSocial")
    __properties = ["schema", "type", "user_id", "access_token", "expires_in", "created", "updated", "profileData", "connection", "isSocial"]

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
    def from_json(cls, json_str: str) -> ExternalProvider:
        """Create an instance of ExternalProvider from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of profile_data
        if self.profile_data:
            _dict['profileData'] = self.profile_data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExternalProvider:
        """Create an instance of ExternalProvider from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExternalProvider.parse_obj(obj)

        _obj = ExternalProvider.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "type": obj.get("type"),
            "user_id": obj.get("user_id"),
            "access_token": obj.get("access_token"),
            "expires_in": obj.get("expires_in"),
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "profile_data": ExternalProviderProfileData.from_dict(obj.get("profileData")) if obj.get("profileData") is not None else None,
            "connection": obj.get("connection"),
            "is_social": obj.get("isSocial")
        })
        return _obj


