# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from pieces_python._pieces_lib.aenum import Enum, no_arg





class ConversationTypeEnum(str, Enum):
    """
    This is a type of conversation, for now just COPILOT.
    """

    """
    allowed enum values
    """
    COPILOT = 'COPILOT'

    @classmethod
    def from_json(cls, json_str: str) -> ConversationTypeEnum:
        """Create an instance of ConversationTypeEnum from a JSON string"""
        return ConversationTypeEnum(json.loads(json_str))


