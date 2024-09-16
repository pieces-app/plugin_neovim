from enum import Enum
import re
from typing import Optional

class VersionChecker:
    def __init__(self, min_version: str, max_version: str, pieces_os_version:str):
        self.min_version = min_version
        self.max_version = max_version
        self.pieces_os_version = pieces_os_version

    @staticmethod
    def _parse_version(version_str):
        """Parse a version string into a tuple of integers and pre-release labels."""
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:[-.](\S+))?$', version_str)
        if not match:
            raise ValueError(f"Invalid version format: {version_str}")

        major, minor, patch, pre_release = match.groups()
        version_tuple = (int(major), int(minor), int(patch))
        pre_release_tuple = tuple(pre_release.split('.')) if pre_release else ()
        return version_tuple, pre_release_tuple

    def version_check(self):
        """Check if the Pieces OS version is within the supported range."""
        # Parse version numbers
        os_version_parsed, os_pre_release = self._parse_version(self.pieces_os_version)
        min_version_parsed, min_pre_release = self._parse_version(self.min_version)
        max_version_parsed, max_pre_release = self._parse_version(self.max_version)

        # Determine compatibility
        if (os_version_parsed < min_version_parsed or
            (os_version_parsed == min_version_parsed and os_pre_release < min_pre_release)):
            return VersionCheckResult(False, UpdateEnum.PiecesOS)
        elif (os_version_parsed > max_version_parsed or
              (os_version_parsed == max_version_parsed and os_pre_release >= max_pre_release)):
            return VersionCheckResult(False, UpdateEnum.Plugin)

        return VersionCheckResult(True)

    @classmethod
    def compare(cls, v1:str, v2:str):
        """Compare two version strings.

        Returns:
            -1 if v1 < v2
             0 if v1 == v2
             1 if v1 > v2
        """
        v1_parsed, v1_pre_release = cls._parse_version(v1)
        v2_parsed, v2_pre_release = cls._parse_version(v2)
        
        # Compare the major, minor, and patch versions
        if v1_parsed < v2_parsed:
            return -1
        elif v1_parsed > v2_parsed:
            return 1
        
        # If major, minor, and patch versions are equal, compare pre-release labels
        if v1_pre_release < v2_pre_release:
            return -1
        elif v1_pre_release > v2_pre_release:
            return 1
        
        return 0


class UpdateEnum(Enum):
    PiecesOS = 1
    Plugin = 2

class VersionCheckResult:
    """Result of the version check."""
    def __init__(self, compatible, update:Optional[UpdateEnum]=None):
        self.compatible = compatible
        self.update = update
