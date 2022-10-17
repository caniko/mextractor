from typing import Optional

import click
from pydantic import DirectoryPath

from mextractor.constants import VIDEO_SUFFIXES
from mextractor.workflow import mextract_videos_in_subdirs


@click.group
def mextractor_cli():
    pass


@mextractor_cli.command()
@click.argument("root_dir", required=True, type=str)
@click.option(
    "-s",
    "--suffix",
    "video_file_suffix",
    help=f"Suffix of the video files in the sub directories, leaving undefined will fallback to all video suffixes {VIDEO_SUFFIXES}",
    type=str,
)
def video_subdirs(root_dir: DirectoryPath, video_file_suffix: Optional[str] = None) -> None:
    mextract_videos_in_subdirs(root_dir, video_file_suffix)
