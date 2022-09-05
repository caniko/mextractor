from mextractor.base import MextractorMetadata
from mextractor.workflow import extract_and_dump_video
from tests import STATICS_PATH, OUTPUT_PATH

TEST_VIDEO_PATH = STATICS_PATH / "mouse_in_box.mp4"


def test_video():
    metadata = extract_and_dump_video(
        dump_dir=OUTPUT_PATH, path_to_video=TEST_VIDEO_PATH, include_image=True, lossy_compress_image=True
    )

    loaded_metadata = MextractorMetadata.load(mextractor_dir=OUTPUT_PATH / f"{metadata.name}.mextractor")
    assert loaded_metadata
    assert loaded_metadata.image is not None


def test_video():
    metadata = extract_and_dump_video(dump_dir=OUTPUT_PATH, path_to_video=TEST_VIDEO_PATH, include_image=False)

    loaded_metadata = MextractorMetadata.load(mextractor_dir=OUTPUT_PATH / f"{metadata.name}.mextractor")
    assert loaded_metadata
    assert loaded_metadata.image is None
