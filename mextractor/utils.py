import cv2
from pydantic import DirectoryPath
from pydantic_numpy import NDArray


def dump_image(frame: NDArray, dump_path: DirectoryPath, name: str, lossy_compress_image: bool = True):
    if lossy_compress_image:
        image_filename = f"{name}-image.jpeg"
        cv2.imwrite(str(dump_path / image_filename), frame)
    else:
        image_filename = f"{name}-image.png"
        cv2.imwrite(
            str(dump_path / image_filename),
            frame,
            [cv2.IMWRITE_PNG_COMPRESSION, 9],
        )
