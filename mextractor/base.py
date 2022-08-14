from functools import cached_property
from pathlib import Path

import webp
from numpy._typing import NDArray
from pydantic import FilePath
from pydantic_yaml import YamlModel
from ruamel.yaml import YAML


class _BaseMextractorMetadata(YamlModel):
    resolution: tuple[int, int]
    webp_image: bytes
    path: Path
    bytes: int

    class Config:
        keep_untouched = (cached_property,)
        frozen = True

    def dump(self, path: Path) -> bool:
        yaml = YAML()
        with open(path, "w") as out_yaml:
            yaml.dump(self.dict(), out_yaml)
        return True

    @cached_property
    def image(self) -> NDArray:
        webp_data = webp.WebPData.from_buffer(self.webp_image)
        return webp_data.decode(color_mode=webp.WebPColorMode.BGR)


def webp_compress_image(image_array: NDArray) -> bytes:
    """Compresses the image array to WEBP format"""
    pic = webp.WebPPicture.from_numpy(image_array)
    config = webp.WebPConfig.new(preset=webp.WebPPreset.PHOTO, quality=70)
    return bytes(pic.encode(config).buffer())


def generic_media_metadata_dict(path_to_media: FilePath, image: NDArray) -> dict[str, bytes | int | Path]:
    return {"webp_image": webp_compress_image(image), "bytes": path_to_media.stat().st_size, "path": path_to_media}
