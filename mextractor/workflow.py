import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from shutil import rmtree
from typing import Optional

from pydantic import FilePath, DirectoryPath, validate_arguments

from mextractor.base import MextractorMetadata
from mextractor.constants import VIDEO_SUFFIXES
from mextractor.extractors import extract_image, extract_video, extract_video_frame
from mextractor.utils import dump_image


def extract_and_dump_image(
    dump_dir: DirectoryPath,
    path_to_image: FilePath,
    include_image: bool = True,
    lossy_compress_image: bool = True,
) -> MextractorMetadata:
    metadata = extract_image(path_to_image, include_image)
    metadata.dump(dump_dir, include_image, lossy_compress_image)
    return metadata


def extract_and_dump_video(
    dump_dir: DirectoryPath,
    path_to_video: FilePath,
    include_image: bool = True,
    lossy_compress_image: bool = True,
) -> MextractorMetadata:
    metadata = extract_video(path_to_video, include_image)
    metadata.dump(dump_dir, include_image, lossy_compress_image)
    return metadata


@validate_arguments
def mextract_videos_in_subdirs(
    root_dir: DirectoryPath, video_file_suffix: Optional[str] = None, only_frame: bool = False
) -> None:
    """
    Copy directory to a new directory while extracting media info and a single frame from videos in subdirectories
    """
    new_root = root_dir.with_name(f"{root_dir.name}_mextracted")
    if new_root.exists():
        rmtree(new_root)
    new_root.mkdir()

    with ThreadPoolExecutor() as executor:
        for source_path in root_dir.glob("**/*.*"):
            dest_path = new_root / source_path.relative_to(root_dir)
            dest_dir = dest_path.parent

            os.makedirs(dest_dir, exist_ok=True)

            if video_file_suffix and video_file_suffix in dest_path.suffix or dest_path.suffix in VIDEO_SUFFIXES:
                if only_frame:
                    dump_image(
                        extract_video_frame(source_path),
                        dest_dir,
                        source_path.stem,
                        lossy_compress_image=False,
                    )
                else:
                    executor.submit(extract_and_dump_video, dest_dir, source_path, include_image=True)
            else:
                executor.submit(shutil.copy, source_path, dest_path)
