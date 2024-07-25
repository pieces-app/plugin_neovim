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





class ApplicationNameEnum(str, Enum):
    """
    This is a running enumeration for the Names of all the Applications that can be Registered
    """

    """
    allowed enum values
    """
    SUBLIME = 'SUBLIME'
    VS_CODE = 'VS_CODE'
    JETBRAINS = 'JETBRAINS'
    FIREFOX_ADDON_MV2 = 'FIREFOX_ADDON_MV2'
    FIREFOX_ADDON_MV3 = 'FIREFOX_ADDON_MV3'
    SAFARI_EXTENSION_MV2 = 'SAFARI_EXTENSION_MV2'
    SAFARI_EXTENSION_MV3 = 'SAFARI_EXTENSION_MV3'
    PIECES_FOR_DEVELOPERS = 'PIECES_FOR_DEVELOPERS'
    PIECES_FOR_DEVELOPERS_CLI = 'PIECES_FOR_DEVELOPERS_CLI'
    OS_SERVER = 'OS_SERVER'
    GOOGLE_CHROME_EXTENSION_MV2 = 'GOOGLE_CHROME_EXTENSION_MV2'
    GOOGLE_CHROME_EXTENSION_MV3 = 'GOOGLE_CHROME_EXTENSION_MV3'
    ULTRA_EDIT = 'ULTRA_EDIT'
    ATOM_PACKAGE = 'ATOM_PACKAGE'
    ADOBE_ILLUSTRATOR_PIECES_COLOR_SHARE = 'ADOBE_ILLUSTRATOR_PIECES_COLOR_SHARE'
    MICROSOFT_TEAMS = 'MICROSOFT_TEAMS'
    CHAT_GPT = 'CHAT_GPT'
    OBSIDIAN = 'OBSIDIAN'
    JUPYTER_HUB = 'JUPYTER_HUB'
    VISUAL_STUDIO = 'VISUAL_STUDIO'
    MICROSOFT_EDGE = 'MICROSOFT_EDGE'
    BRAVE = 'BRAVE'
    GOOGLE_CHAT = 'GOOGLE_CHAT'
    SLACK = 'SLACK'
    AZURE_DATA_STUDIO = 'AZURE_DATA_STUDIO'
    OPEN_SOURCE = 'OPEN_SOURCE'
    R_STUDIO = 'R_STUDIO'
    VIM = 'VIM'
    NOTION = 'NOTION'
    GITHUB_DESKTOP = 'GITHUB_DESKTOP'
    RAYCAST = 'RAYCAST'
    REPLIT = 'REPLIT'
    ALFRED = 'ALFRED'
    FIGMA = 'FIGMA'
    SKETCH = 'SKETCH'
    ADOBE_ILLUSTRATOR = 'ADOBE_ILLUSTRATOR'
    NOTEPAD_PLUS_PLUS = 'NOTEPAD_PLUS_PLUS'
    EMBEETLE = 'EMBEETLE'
    ECLIPSE = 'ECLIPSE'
    X_CODE = 'X_CODE'
    NETBEANS = 'NETBEANS'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def from_json(cls, json_str: str) -> ApplicationNameEnum:
        """Create an instance of ApplicationNameEnum from a JSON string"""
        return ApplicationNameEnum(json.loads(json_str))


