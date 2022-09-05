from typing import Optional

import cv2
from pydantic import FilePath, validate_arguments
from pydantic_numpy import NDArrayUint8

from mextractor.base import MextractorMetadata


def _generic_media_metadata_dict(path_to_media: FilePath, image_array: Optional[NDArrayUint8] = None) -> dict:
    return {"bytes": path_to_media.stat().st_size, "path": path_to_media, "image": image_array}


@validate_arguments
def extract_image(path_to_image: FilePath, include_image: bool = True, greyscale: bool = True) -> MextractorMetadata:
    image = cv2.imread(str(path_to_image), 0 if greyscale else -1)

    return MextractorMetadata(
        name=path_to_image.stem,
        resolution=(image.shape[1], image.shape[0]),
        **_generic_media_metadata_dict(path_to_image, image if include_image else None),
    )


@validate_arguments
def extract_video(
    path_to_video: FilePath,
    include_image: bool = True,
    frame_to_extract_time: str | int = "middle",
    greyscale: bool = True,
) -> MextractorMetadata:
    try:
        import ffmpeg
    except ImportError:
        msg = "Extra to extract video metadata not installed. Install by:\npip install mextractor[video-extract]"
        raise ImportError(msg)

    cap = cv2.VideoCapture(str(path_to_video), 0 if greyscale else -1)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    msg = (
        f"frame_to_extract_time can only be defined as halfway, start, end, or integer; "
        f"not {type(frame_to_extract_time)}"
    )
    if isinstance(frame_to_extract_time, str):
        if (frame_to_extract_time := frame_to_extract_time.lower()) == "middle":
            target_frame_index = round(frame_count / 2.0)
        elif frame_to_extract_time == "start" or frame_to_extract_time == "beginning":
            target_frame_index = 0
        elif frame_to_extract_time == "end":
            target_frame_index = frame_count
        else:
            raise ValueError(msg)
    elif isinstance(frame_to_extract_time, int):
        target_frame_index = frame_to_extract_time
    else:
        raise TypeError(msg)

    cap.set(1, target_frame_index - 1)
    res, frame = cap.read()

    assert res, f"Could not extract frame from media, {path_to_video}"

    ffmpeg_metadata = ffmpeg.probe(path_to_video)["streams"][0]

    if "/" in ffmpeg_metadata["avg_frame_rate"]:
        numerator, denominator = ffmpeg_metadata["avg_frame_rate"].split("/")
        average_fps = int(numerator) / int(denominator)
    else:
        average_fps = float(ffmpeg_metadata["avg_frame_rate"])

    return MextractorMetadata(
        name=path_to_video.stem,
        resolution=(ffmpeg_metadata["width"], ffmpeg_metadata["height"]),
        frames=ffmpeg_metadata["nb_frames"],
        average_fps=average_fps,
        seconds=ffmpeg_metadata["duration"],
        **_generic_media_metadata_dict(path_to_video, frame if include_image else None),
    )