from pydantic import FilePath

from mextractor.base import _BaseMextractorMetadata, generic_media_metadata_dict


class MextractorVideoMetadata(_BaseMextractorMetadata):
    fps: float
    frames: int
    seconds: float


def extract_video(path_to_video: FilePath, frame_time: str | int = "middle") -> MextractorVideoMetadata:
    try:
        import cv2, ffmpeg
    except ImportError:
        msg = "Install extractor extra to extract metadata"
        raise ImportError(msg)

    cap = cv2.VideoCapture(str(path_to_video))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    msg = f"frame_time can only be defined as halfway, start, end, or integer; " f"not {type(frame_time)}"
    if isinstance(frame_time, str):
        if (frame_time := frame_time.lower()) == "middle":
            target_frame_index = round(frame_count / 2.0)
        elif frame_time == "start" or frame_time == "beginning":
            target_frame_index = 0
        elif frame_time == "end":
            target_frame_index = frame_count
        else:
            raise ValueError(msg)
    elif isinstance(frame_time, int):
        target_frame_index = frame_time
    else:
        raise TypeError(msg)

    cap.set(1, target_frame_index - 1)
    res, frame = cap.read()

    assert res, f"Could not extract frame from media, {path_to_video}"

    ffmpeg_metadata = ffmpeg.probe(path_to_video)["streams"][0]

    if "/" in ffmpeg_metadata["avg_frame_rate"]:
        numerator, denominator = ffmpeg_metadata["avg_frame_rate"].split("/")
        fps = int(numerator) / int(denominator)
    else:
        fps = float(ffmpeg_metadata["avg_frame_rate"])

    return MextractorVideoMetadata(
        resolution=(ffmpeg_metadata["width"], ffmpeg_metadata["height"]),
        frames=ffmpeg_metadata["nb_frames"],
        fps=fps,
        seconds=ffmpeg_metadata["duration"],
        **generic_media_metadata_dict(path_to_video, frame),
    )