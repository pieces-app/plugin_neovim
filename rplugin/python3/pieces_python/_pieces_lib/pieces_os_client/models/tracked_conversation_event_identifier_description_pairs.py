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
from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictStr, validator
from pieces_python._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class TrackedConversationEventIdentifierDescriptionPairs(BaseModel):
    """
    These are all of the available event types that are permitted in an object pair notation.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    conversation_created: Optional[StrictStr] = Field(default=None, description="The key value pair for an conversation being created.")
    conversation_referenced: Optional[StrictStr] = Field(default=None, description="This means that an conversation was view/used while the user was looking at the default view.")
    conversation_deleted: Optional[StrictStr] = Field(default=None, description="A conversation was deleted")
    conversation_summary_annotation_generated_by_the_user: Optional[StrictStr] = Field(default=None, description="A conversation summary was generated by the user")
    conversation_name_updated_by_the_system: Optional[StrictStr] = Field(default=None, description="A conversation was renamed by the system")
    conversation_name_updated_by_the_user: Optional[StrictStr] = Field(default=None, description="A conversation was renamed by the user")
    conversation_summary_annotation_generated_by_the_system: Optional[StrictStr] = Field(default=None, description="A conversation summary was generated")
    __properties = ["schema", "conversation_created", "conversation_referenced", "conversation_deleted", "conversation_summary_annotation_generated_by_the_user", "conversation_name_updated_by_the_system", "conversation_name_updated_by_the_user", "conversation_summary_annotation_generated_by_the_system"]

    @validator('conversation_created')
    def conversation_created_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_was_created'):
            raise ValueError("must be one of enum values ('a_conversation_was_created')")
        return value

    @validator('conversation_referenced')
    def conversation_referenced_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_was_referenced_by_the_user'):
            raise ValueError("must be one of enum values ('a_conversation_was_referenced_by_the_user')")
        return value

    @validator('conversation_deleted')
    def conversation_deleted_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_was_deleted'):
            raise ValueError("must be one of enum values ('a_conversation_was_deleted')")
        return value

    @validator('conversation_summary_annotation_generated_by_the_user')
    def conversation_summary_annotation_generated_by_the_user_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_summary_annotation_was_generated_by_the_user'):
            raise ValueError("must be one of enum values ('a_conversation_summary_annotation_was_generated_by_the_user')")
        return value

    @validator('conversation_name_updated_by_the_system')
    def conversation_name_updated_by_the_system_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_was_renamed_by_the_system'):
            raise ValueError("must be one of enum values ('a_conversation_was_renamed_by_the_system')")
        return value

    @validator('conversation_name_updated_by_the_user')
    def conversation_name_updated_by_the_user_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_was_renamed_by_the_user'):
            raise ValueError("must be one of enum values ('a_conversation_was_renamed_by_the_user')")
        return value

    @validator('conversation_summary_annotation_generated_by_the_system')
    def conversation_summary_annotation_generated_by_the_system_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('a_conversation_summary_annotation_was_generated_by_the_system'):
            raise ValueError("must be one of enum values ('a_conversation_summary_annotation_was_generated_by_the_system')")
        return value

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
    def from_json(cls, json_str: str) -> TrackedConversationEventIdentifierDescriptionPairs:
        """Create an instance of TrackedConversationEventIdentifierDescriptionPairs from a JSON string"""
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
    def from_dict(cls, obj: dict) -> TrackedConversationEventIdentifierDescriptionPairs:
        """Create an instance of TrackedConversationEventIdentifierDescriptionPairs from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TrackedConversationEventIdentifierDescriptionPairs.parse_obj(obj)

        _obj = TrackedConversationEventIdentifierDescriptionPairs.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "conversation_created": obj.get("conversation_created"),
            "conversation_referenced": obj.get("conversation_referenced"),
            "conversation_deleted": obj.get("conversation_deleted"),
            "conversation_summary_annotation_generated_by_the_user": obj.get("conversation_summary_annotation_generated_by_the_user"),
            "conversation_name_updated_by_the_system": obj.get("conversation_name_updated_by_the_system"),
            "conversation_name_updated_by_the_user": obj.get("conversation_name_updated_by_the_user"),
            "conversation_summary_annotation_generated_by_the_system": obj.get("conversation_summary_annotation_generated_by_the_system")
        })
        return _obj


