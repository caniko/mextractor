from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from typing import Optional, TypeVar

import webp
from pydantic import FilePath
from pydantic_numpy import NDArray
from pydantic_yaml import YamlModel
from ruamel.yaml import YAML


class _BaseMextractorMetadata(YamlModel, ABC):
    resolution: tuple[int, int]
    path: Path
    bytes: int
    webp_image: Optional[bytes]
    image_array: Optional[NDArray]

    class Config:
        keep_untouched = (cached_property,)
        frozen = True

    @classmethod
    @abstractmethod
    def extract(cls, media_path: FilePath, with_image: bool = True) -> "Metadata":
        ...

    @classmethod
    def extract_and_dump(cls, dump_path: Path, **extract_kwargs) -> None:
        cls.extract(**extract_kwargs).dump(dump_path)

    def dump(self, path: Path) -> bool:
        yaml = YAML()
        with open(path, "w") as out_yaml:
            yaml.dump(self.dict(), out_yaml)
        return True

    @cached_property
    def image(self) -> NDArray | None:
        if self.image_array is not None:
            return self.image_array
        if self.webp_image:
            webp_data = webp.WebPData.from_buffer(self.webp_image)
            return webp_data.decode(color_mode=webp.WebPColorMode.BGR)


Metadata = TypeVar("Metadata", bound=_BaseMextractorMetadata)


def webp_compress_image(image_array: NDArray) -> bytes:
    """Compresses the image array to WEBP format"""
    pic = webp.WebPPicture.from_numpy(image_array)
    config = webp.WebPConfig.new(preset=webp.WebPPreset.PHOTO, quality=70)
    return bytes(pic.encode(config).buffer())


def generic_media_metadata_dict(
    path_to_media: FilePath, image_array: Optional[NDArray], compress_image: bool = True
) -> dict[str, bytes | int | Path]:
    out = {"bytes": path_to_media.stat().st_size, "path": path_to_media}
    if image_array is not None:
        if compress_image:
            out["webp_image"] = webp_compress_image(image_array)
        else:
            out["image_array"] = image_array
    return out
