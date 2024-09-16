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
from pieces_python._pieces_lib.pydantic import BaseModel, Field
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.qgpt_agent_related_routes import QGPTAgentRelatedRoutes

class QGPTAgentRoutes(BaseModel):
    """
    This is apart of the Output and will let the plugin developer know if we reccomend to run specific agent functionality/routes. for instance, related.people, code classification...xyz, for now we start with relatedPeople.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    related: Optional[QGPTAgentRelatedRoutes] = None
    __properties = ["schema", "related"]

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
    def from_json(cls, json_str: str) -> QGPTAgentRoutes:
        """Create an instance of QGPTAgentRoutes from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of related
        if self.related:
            _dict['related'] = self.related.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> QGPTAgentRoutes:
        """Create an instance of QGPTAgentRoutes from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QGPTAgentRoutes.parse_obj(obj)

        _obj = QGPTAgentRoutes.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "related": QGPTAgentRelatedRoutes.from_dict(obj.get("related")) if obj.get("related") is not None else None
        })
        return _obj


