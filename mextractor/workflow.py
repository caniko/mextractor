from pydantic import FilePath, DirectoryPath

from mextractor.base import MextractorMetadata
from mextractor.extractors import extract_image, extract_video


def extract_and_dump_image(
    dump_dir: DirectoryPath,
    path_to_image: FilePath,
    include_image: bool = True,
    greyscale: bool = True,
    lossy_compress_image: bool = True,
) -> MextractorMetadata:
    metadata = extract_image(path_to_image, include_image, greyscale=greyscale)
    metadata.dump(dump_dir, include_image, lossy_compress_image)
    return metadata


def extract_and_dump_video(
    dump_dir: DirectoryPath,
    path_to_video: FilePath,
    include_image: bool = True,
    greyscale: bool = True,
    lossy_compress_image: bool = True,
) -> MextractorMetadata:
    metadata = extract_video(path_to_video, include_image, greyscale=greyscale)
    metadata.dump(dump_dir, include_image, lossy_compress_image)
    return metadata
