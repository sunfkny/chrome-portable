from typing import NamedTuple

from loguru import logger
from typing_extensions import TypeIs


def is_valid_version(version: str | None) -> TypeIs[str]:
    if not version:
        return False
    if len(version.split(".")) != 4:
        logger.error("Bad version parameter passed!")
        return False
    return True


class Version(NamedTuple):
    milestone: int
    branch: int
    build: int
    color: str


def get_version_object(version: str | None):
    if not is_valid_version(version):
        return None

    milestone, _, branch, build = version.split(".")
    milestone = int(milestone)
    branch = int(branch)
    build = int(build)
    colors = ["#3F51B5", "#9C27B0", "#009688", "#03A9F4"]
    color = colors[milestone % len(colors)]
    return Version(
        milestone=milestone,
        branch=branch,
        build=build,
        color=color,
    )
