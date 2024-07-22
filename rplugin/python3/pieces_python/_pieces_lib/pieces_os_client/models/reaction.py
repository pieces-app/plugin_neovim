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
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictBool
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_python._pieces_lib.pieces_os_client.models.reuse_reaction import ReuseReaction
from pieces_python._pieces_lib.pieces_os_client.models.seeded_connector_creation import SeededConnectorCreation

class Reaction(BaseModel):
    """
    This will the the Request body of the Request Endpoint.  Reuse will not be required here because we do NOT know if the user will choose to reuse what we have suggested.  save will however be required because this will let us know if we should save the coppied asset that was first sent over or not.  seed is required, because we will want to know 100% sure what the original suggestion was made against.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    save: StrictBool = Field(default=..., description="This will just be a simple boolean here that will say if the use should save the asset or not.")
    reuse: Optional[ReuseReaction] = None
    seed: SeededConnectorCreation = Field(...)
    __properties = ["schema", "save", "reuse", "seed"]

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
    def from_json(cls, json_str: str) -> Reaction:
        """Create an instance of Reaction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of reuse
        if self.reuse:
            _dict['reuse'] = self.reuse.to_dict()
        # override the default output from pydantic by calling `to_dict()` of seed
        if self.seed:
            _dict['seed'] = self.seed.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Reaction:
        """Create an instance of Reaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Reaction.parse_obj(obj)

        _obj = Reaction.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "save": obj.get("save"),
            "reuse": ReuseReaction.from_dict(obj.get("reuse")) if obj.get("reuse") is not None else None,
            "seed": SeededConnectorCreation.from_dict(obj.get("seed")) if obj.get("seed") is not None else None
        })
        return _obj


