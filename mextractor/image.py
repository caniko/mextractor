from pydantic import FilePath

from mextractor.base import _BaseMextractorMetadata, generic_media_metadata_dict


class MextractorImageMetadata(_BaseMextractorMetadata):
    pass


def extract_image(path_to_image: FilePath) -> MextractorImageMetadata:
    try:
        import cv2
    except ImportError:
        msg = "Install extractor extra to extract metadata"
        raise ImportError(msg)

    image = cv2.imread(str(path_to_image))

    return MextractorImageMetadata(
        resolution=(image.shape[1], image.shape[0]), **generic_media_metadata_dict(path_to_image, image)
    )
