from mextractor.image import MextractorImageMetadata
from tests import STATICS_PATH, OUTPUT_PATH

TEST_IMAGE_PATH = STATICS_PATH / "dworm.png"
IMAGE_METADATA_TEST_DUMP_PATH = OUTPUT_PATH / "image_test_dump.yaml"


def test_image():
    MextractorImageMetadata.extract_and_dump(
        IMAGE_METADATA_TEST_DUMP_PATH, media_path=TEST_IMAGE_PATH, with_image=True
    )

    loaded_metadata = MextractorImageMetadata.parse_file(
        path=IMAGE_METADATA_TEST_DUMP_PATH
    )
    assert loaded_metadata
    assert loaded_metadata.image is not None


def test_image_with_no_image():
    MextractorImageMetadata.extract_and_dump(
        IMAGE_METADATA_TEST_DUMP_PATH, media_path=TEST_IMAGE_PATH, with_image=False
    )

    loaded_metadata = MextractorImageMetadata.parse_file(
        path=IMAGE_METADATA_TEST_DUMP_PATH
    )
    assert loaded_metadata
    assert loaded_metadata.image is None
