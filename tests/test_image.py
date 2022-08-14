from mextractor.image import extract_image, MextractorImageMetadata
from tests import STATICS_PATH, OUTPUT_PATH

IMAGE_METADATA_TEST_DUMP_PATH = OUTPUT_PATH / "image_test_dump.yaml"


def test_image():
    metadata = extract_image(STATICS_PATH / "dworm.png")
    assert metadata
    assert metadata.dump(IMAGE_METADATA_TEST_DUMP_PATH)

    loaded_metadata = MextractorImageMetadata.parse_file(path=IMAGE_METADATA_TEST_DUMP_PATH)
    assert loaded_metadata
