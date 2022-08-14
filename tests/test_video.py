from mextractor.video import MextractorVideoMetadata
from tests import STATICS_PATH, OUTPUT_PATH

TEST_VIDEO_PATH = STATICS_PATH / "mouse_in_box.mp4"
VIDEO_METADATA_TEST_DUMP_PATH = OUTPUT_PATH / "video_test_dump.yaml"


def test_video():
    MextractorVideoMetadata.extract_and_dump(VIDEO_METADATA_TEST_DUMP_PATH, media_path=TEST_VIDEO_PATH, with_image=True)

    loaded_metadata = MextractorVideoMetadata.parse_file(path=VIDEO_METADATA_TEST_DUMP_PATH)
    assert loaded_metadata
    assert loaded_metadata.image is not None


def test_video_with_no_video():
    MextractorVideoMetadata.extract_and_dump(
        VIDEO_METADATA_TEST_DUMP_PATH, media_path=TEST_VIDEO_PATH, with_image=False
    )

    loaded_metadata = MextractorVideoMetadata.parse_file(path=VIDEO_METADATA_TEST_DUMP_PATH)
    assert loaded_metadata
    assert loaded_metadata.image is None
