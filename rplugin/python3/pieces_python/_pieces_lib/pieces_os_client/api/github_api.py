# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import re  # noqa: F401
import io
import warnings

from pieces_python._pieces_lib.pydantic import validate_arguments, ValidationError

from typing_extensions import Annotated
from pieces_python._pieces_lib.pydantic import Field, StrictBool

from typing import Optional

from pieces_python._pieces_lib.pieces_os_client.models.seeded_github_gists_import import SeededGithubGistsImport
from pieces_python._pieces_lib.pieces_os_client.models.seeds import Seeds

from pieces_python._pieces_lib.pieces_os_client.api_client import ApiClient
from pieces_python._pieces_lib.pieces_os_client.api_response import ApiResponse
from pieces_python._pieces_lib.pieces_os_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class GithubApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def import_github_gists(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_github_gists_import : Optional[SeededGithubGistsImport] = None, **kwargs) -> Seeds:  # noqa: E501
        """/github/gists/import [POST]  # noqa: E501

        This will attempt to get all the gist availble and return them to the user as a DiscoveredAssets.  if automatic is true we will automatically create the asset.  v1. will just get all the users' gists. implemented. v2. can get specific a public gist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.import_github_gists(automatic, seeded_github_gists_import, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_github_gists_import: 
        :type seeded_github_gists_import: SeededGithubGistsImport
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Seeds
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the import_github_gists_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.import_github_gists_with_http_info(automatic, seeded_github_gists_import, **kwargs)  # noqa: E501

    @validate_arguments
    def import_github_gists_with_http_info(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_github_gists_import : Optional[SeededGithubGistsImport] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/github/gists/import [POST]  # noqa: E501

        This will attempt to get all the gist availble and return them to the user as a DiscoveredAssets.  if automatic is true we will automatically create the asset.  v1. will just get all the users' gists. implemented. v2. can get specific a public gist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.import_github_gists_with_http_info(automatic, seeded_github_gists_import, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_github_gists_import: 
        :type seeded_github_gists_import: SeededGithubGistsImport
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(Seeds, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'automatic',
            'seeded_github_gists_import'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method import_github_gists" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('automatic') is not None:  # noqa: E501
            _query_params.append(('automatic', _params['automatic']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_github_gists_import'] is not None:
            _body_params = _params['seeded_github_gists_import']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "Seeds",
            '412': "str",
            '500': "str",
            '511': "str",
        }

        return self.api_client.call_api(
            '/github/gists/import', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
