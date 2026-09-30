import pytest

from mextractor.base import load_image
from mextractor.extractors import extract_image
from mextractor.workflow import extract_and_dump_image
from tests import OUTPUT_PATH, STATICS_PATH

TEST_IMAGE_PATH = STATICS_PATH / "dworm.png"


def test_image():
    metadata = extract_and_dump_image(
        dump_dir=OUTPUT_PATH,
        path_to_image=TEST_IMAGE_PATH,
        include_image=True,
        lossy_compress_image=True,
    )

    loaded_metadata = load_image(mextractor_dir=OUTPUT_PATH / f"{metadata.name}.mextractor")
    assert loaded_metadata
    assert loaded_metadata.image is not None


def test_image_with_no_image():
    metadata = extract_and_dump_image(dump_dir=OUTPUT_PATH, path_to_image=TEST_IMAGE_PATH, include_image=False)

    loaded_metadata = load_image(mextractor_dir=OUTPUT_PATH / f"{metadata.name}.mextractor")
    assert loaded_metadata
    assert loaded_metadata.image is None


def test_invalid_image_is_rejected(tmp_path):
    source = tmp_path / "broken.png"
    source.write_bytes(b"not an image")
    with pytest.raises(ValueError, match="Could not decode image"):
        extract_image(source)
