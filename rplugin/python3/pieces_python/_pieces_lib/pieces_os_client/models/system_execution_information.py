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



from pieces_python._pieces_lib.pydantic import BaseModel, Field, StrictInt, StrictStr
from pieces_python._pieces_lib.pieces_os_client.models.system_execution_cpu_information import SystemExecutionCpuInformation

class SystemExecutionInformation(BaseModel):
    """
    This is system information that we are able to get from the users machine(rust package TBD). TODO potentially pull this out of TLP.  # noqa: E501
    """
    memory: StrictInt = Field(...)
    os: StrictStr = Field(...)
    kernel: StrictStr = Field(...)
    cpu: SystemExecutionCpuInformation = Field(...)
    __properties = ["memory", "os", "kernel", "cpu"]

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
    def from_json(cls, json_str: str) -> SystemExecutionInformation:
        """Create an instance of SystemExecutionInformation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of cpu
        if self.cpu:
            _dict['cpu'] = self.cpu.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SystemExecutionInformation:
        """Create an instance of SystemExecutionInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SystemExecutionInformation.parse_obj(obj)

        _obj = SystemExecutionInformation.parse_obj({
            "memory": obj.get("memory"),
            "os": obj.get("os"),
            "kernel": obj.get("kernel"),
            "cpu": SystemExecutionCpuInformation.from_dict(obj.get("cpu")) if obj.get("cpu") is not None else None
        })
        return _obj


