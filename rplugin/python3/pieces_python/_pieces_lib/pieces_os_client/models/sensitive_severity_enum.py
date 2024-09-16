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





class SensitiveSeverityEnum(str, Enum):
    """
    This is the enum used to describe the severity of our sensitive model. ie low, moderate, high
    """

    """
    allowed enum values
    """
    LOW = 'LOW'
    MODERATE = 'MODERATE'
    HIGH = 'HIGH'

    @classmethod
    def from_json(cls, json_str: str) -> SensitiveSeverityEnum:
        """Create an instance of SensitiveSeverityEnum from a JSON string"""
        return SensitiveSeverityEnum(json.loads(json_str))


