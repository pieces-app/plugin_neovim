from typing import Optional
from pieces_os_client.wrapper import PiecesClient
from pieces_os_client.models.seeded_connector_connection import SeededConnectorConnection
from pieces_os_client.models.seeded_tracked_application import SeededTrackedApplication
from pieces_os_client.wrapper.version_compatibility import VersionCheckResult
from pieces_os_client.api.applications_api import ApplicationsApi
from pieces_os_client.models.application_name_enum import ApplicationNameEnum
from ._version import __version__
import pynvim
import json
import urllib.request
import os
import webbrowser
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


class Settings:
    # Initialize class variables
    nvim: pynvim.Nvim
    os: str

    api_client: PiecesClient
    version_compatibility: Optional[VersionCheckResult] = None

    @classmethod
    def set_model_name(cls, value):
        if value in cls.api_client.available_models_names:
            cls.api_client.model_name = value
            cls.update_settings(model_name=value)

    @classmethod
    def get_config(cls, config):
        lua_code = f"""
        local config = require('pieces.config')
        return config.{config}
        """
        out = cls.nvim.exec_lua(lua_code)
        return out

    @classmethod
    def load_config(cls) -> None:
        """
                Load the lua configrations
        """

        # Setting up the host and the os
        setattr(cls, "os", cls.get_config("os"))

        cls.api_client = PiecesClient(
            seeded_connector=SeededConnectorConnection(
                application=SeededTrackedApplication(
                    name="VIM",
                    platform=cls.os,
                    version=__version__)),
            connect_websockets=False)

        cls.pieces_data_dir = cls.nvim.call('stdpath', 'data')
        cls.plugin_dir = os.path.join(cls.pieces_data_dir, 'Pieces')
        cls.settings_file = os.path.join(cls.plugin_dir, "settings.json")
        if not os.path.exists(cls.plugin_dir):
            os.makedirs(cls.plugin_dir)

    @classmethod
    def get_copilot_mode(cls):
        return cls.get_config('copilot_mode')

    @classmethod
    def load_settings(cls):
        try:
            with open(cls.settings_file, 'r') as file:
                data = json.load(file)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    @classmethod
    def update_settings(cls, **kwargs):
        data = cls.load_settings()
        data.update(kwargs)

        with open(cls.settings_file, "w") as f:
            json.dump(data, f)

    @staticmethod
    def get_latest_tag():
        with urllib.request.urlopen("https://api.github.com/repos/pieces-app/plugin_neo_vim/tags") as response:
            if response.status == 200:
                data = response.read()
                tags = json.loads(data)

                if tags:
                    return tags[0]['name']

    @classmethod
    def get_os_id(cls):
        if cls._os_id:
            return cls._os_id
        if not hasattr(cls.api_client, "applications_api"):
            setattr(cls.api_client, "applications_api",
                    ApplicationsApi(cls.api_client.api_client))
        for app in cls.api_client.applications_api.applications_snapshot().iterable:
            if app.name == ApplicationNameEnum.OS_SERVER:
                cls._os_id = app.id
                return app.id

    @classmethod
    def open_website(cls, url: str):
        from .auth.auth_user import AuthUser
        if (not cls.api_client.is_pos_stream_running) and ("pieces.app" not in url):
            return webbrowser.open(url)
        para = {}
        if AuthUser.user_profile:
            para["user"] = AuthUser.user_profile.id
        _id = cls.get_os_id()
        if _id:
            para["os"] = _id

        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(para)

        url_parts[4] = urlencode(query)
        new_url = urlunparse(url_parts)
        print(new_url)
        webbrowser.open(new_url)
