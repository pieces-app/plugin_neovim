from pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from pieces_os_client.wrapper.websockets import HealthWS
from pieces_os_client.wrapper.version_compatibility import UpdateEnum, VersionChecker
from .settings import Settings
import os

PIECES_OS_MIN_VERSION = "12.0.0"  # Minium version (12.0.0)
PIECES_OS_MAX_VERSION = "13.0.0"  # Maxium version (13.0.0)


def convert_to_lua_table(python_dict):
    """
    Convert a Python dictionary to a Lua table representation.
    Does not support objects and does not support lists except list of strings.
    """
    def convert_value(value):
        if isinstance(value, dict):
            return convert_to_lua_table(value)
        elif isinstance(value, str):
            return f'[=[{value}]=]'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, list):
            return "{" + ", ".join(f'"{val}"' for val in value) + "}"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            raise TypeError(f"Unsupported data type: {type(value)}")

    out = "{"
    for key, value in python_dict.items():
        lua_key = f'["{key}"]' if isinstance(key, str) else key
        lua_value = convert_value(value)
        out += f"{lua_key} = {lua_value}, "
    return out.rstrip(', ') + "}"


def on_copilot_message(message):
    if message.question:
        answers = message.question.answers.iterable

        for answer in answers:
            if not answer.text:
                continue
            text = answer.text
            if text == "\n":
                Settings.nvim.async_call(Settings.nvim.exec_lua, f"""
                        require("pieces.copilot").add_line()""")
                continue
            Settings.nvim.async_call(Settings.nvim.exec_lua, f"""
                    require("pieces.copilot").append_to_chat([=[{text}]=],"ASSISTANT")
            """)

    if message.status == "COMPLETED":
        Settings.nvim.async_call(Settings.nvim.exec_lua, f"""
                require("pieces.copilot").completed(true)
        """)
        Settings.api_client.copilot.chat = BasicChat(message.conversation)
    elif message.status == "FAILED":
        Settings.nvim.async_call(Settings.nvim.exec_lua, f"""
                require("pieces.copilot").completed(true)
        """)
        return  # TODO: Add a better error message


def check_compatibility(notify_if_pos_off=False):
    if not Settings.version_compatibility:
        if not Settings.api_client.is_pieces_running():
            if notify_if_pos_off:
                Settings.nvim.exec_lua(
                    "require('pieces.utils').notify_pieces_os()")
            return False

        Settings.version_compatibility = VersionChecker(
            PIECES_OS_MIN_VERSION,
            PIECES_OS_MAX_VERSION,
            Settings.api_client.version).version_check()

    if not Settings.version_compatibility.compatible:
        plugin = "Pieces OS" if Settings.version_compatibility.update == UpdateEnum.PiecesOS else "the Neovim Pieces plugin"
        Settings.nvim.async_call(
            Settings.nvim.err_write, f"Please update {plugin}\n")
        return False
    else:
        return True

def check_login() -> bool:
    from .auth import Auth

    if not Auth.user_profile:
        Settings.nvim.exec_lua("require('pieces.utils').notify_login()")
        return False
    return True

def is_pieces_opened(bypass_login=False):
    """
    Decorator that checks if POS is running and shows a notification if it's not.
    It also checks if the user is logged in or allows bypass via parameter.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_compatibility(True):
                return

            login_state = check_login() or bypass_login
            if Settings.api_client.is_pos_stream_running and login_state:
                return func(*args, **kwargs)
            else:
                # Run the health request to check if the server is running
                if Settings.api_client.is_pieces_running():
                    if not login_state:
                        return
                    HealthWS.get_instance().start()
                    return func(*args, **kwargs)
                else:
                    return Settings.nvim.exec_lua("require('pieces.utils').notify_pieces_os()")
        return wrapper
    return decorator


def install_pieces_os():
    """
    Install Pieces OS based on the platform
    """

    if Settings.api_client.local_os == "WINDOWS":
        Settings.open_website(
            f"https://builds.pieces.app/stages/production/appinstaller/"
            "os_server.appinstaller?"
            f"product={Settings.api_client.tracked_application.name.value}"
            "&download=true")

    elif Settings.api_client.local_os == "LINUX":
        Settings.open_website("https://snapcraft.io/pieces-os")
        return

    elif Settings.api_client.local_os == "MACOS":
        arch = os.uname().machine
        pkg_url = (
            "https://builds.pieces.app/stages/production/macos_packaging/pkg-pos-launch-only"
            f"{'-arm64' if arch == 'arm64' else ''}/download?"
            f"product={Settings.api_client.tracked_application.name.value}"
            "&download=true"
        )
        Settings.open_website(pkg_url)

    else:
        raise ValueError("Invalid platform")
