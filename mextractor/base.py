import logging
import shutil
from functools import cached_property
from typing import Optional

import cv2
from pydantic import BaseModel, DirectoryPath, FilePath
from pydantic_numpy import NDArrayUint8
from ruamel.yaml import YAML

from mextractor.constants import DUMP_PATH_SUFFIX
from mextractor.utils import dump_image

logger = logging.getLogger()


class MextractorMetadata(BaseModel):
    name: str
    resolution: tuple[int, int]
    average_fps: Optional[float]
    video_length_in_seconds: Optional[float]

    image: Optional[NDArrayUint8]

    class Config:
        keep_untouched = (cached_property,)
        frozen = True

    @classmethod
    def load(cls, mextractor_dir: DirectoryPath) -> "MextractorMetadata":
        image_array: Optional[NDArrayUint8] = None
        for file in mextractor_dir.iterdir():
            if "-image" not in file.stem:
                continue

            if image_array is not None:
                msg = f"More than one image in mextractor directory:\n  {mextractor_dir}"
                raise ValueError(msg)
            image_array = cv2.imread(str(file))

        metadata_path: FilePath
        for file in mextractor_dir.iterdir():
            if "-metadata" in file.stem:
                metadata_path: FilePath = file
                break
        else:  # no break
            msg = "Could not find metadata file inside mextractor directory"
            raise ValueError(msg)

        yaml = YAML()
        with open(metadata_path, "r") as in_yaml:
            return cls(**yaml.load(in_yaml), image=image_array)

    def dump(
        self,
        dump_dir: DirectoryPath,
        include_image: bool = True,
        lossy_compress_image: bool = True,
    ) -> DirectoryPath:
        dump_path = dump_dir / f"{self.name}{DUMP_PATH_SUFFIX}"
        if dump_path.exists():
            shutil.rmtree(dump_path)
        dump_path.mkdir()

        metadata = self.dict(exclude={"image"}, exclude_unset=True)

        if include_image:
            dump_image(self.image, dump_path, self.name, lossy_compress_image)

        yaml = YAML()
        with open(dump_path / f"{self.name}-metadata.yaml", "w") as out_yaml:
            yaml.dump(metadata, out_yaml)
        return dump_dir

    @property
    def fps(self) -> float | None:
        if self.average_fps:
            logger.debug("Frame per second (FPS) from video is an average")
            return self.average_fps


load = MextractorMetadata.load
