from ._version import __version__
import pynvim
import pip


def update_sdks():
    pip.main(["install", "pieces_os_client", "--upgrade"])


MIN_SDKS_VERSION = "4.4.1"
try:
    from pieces_os_client import __version__ as pieces_os_client_version

    try:  # If there is any issue in the version checker then it is outdated
        from pieces_os_client.wrapper.version_compatibility import VersionChecker

        VersionChecker.compare(
            "1.0.0", "1.0.0"
        )  # Check also that the compare is working too
    except (AttributeError, ModuleNotFoundError):
        update_sdks()
        raise ModuleNotFoundError

    if (
        VersionChecker.compare(pieces_os_client_version, MIN_SDKS_VERSION) < 0
    ):  # We need to be above 4.0.0
        update_sdks()
        raise ModuleNotFoundError
    from .main import Pieces
except ModuleNotFoundError:
    pip.main(["install", "pieces_os_client"])
    from .main import Pieces
