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





class PersonAccessScopedEnum(str, Enum):
    """
    This is an enum that will help provide information around what permission this person has in relate to their scope.
    """

    """
    allowed enum values
    """
    OWNER = 'OWNER'
    EDITOR = 'EDITOR'
    COMMENTER = 'COMMENTER'
    VIEWER = 'VIEWER'

    @classmethod
    def from_json(cls, json_str: str) -> PersonAccessScopedEnum:
        """Create an instance of PersonAccessScopedEnum from a JSON string"""
        return PersonAccessScopedEnum(json.loads(json_str))


