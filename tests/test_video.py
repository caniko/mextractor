from mextractor.video import extract_video, MextractorVideoMetadata
from tests import STATICS_PATH, OUTPUT_PATH

VIDEO_METADATA_TEST_DUMP_PATH = OUTPUT_PATH / "video_test_dump.yaml"


def test_video():
    metadata = extract_video(STATICS_PATH / "mouse_in_box.mp4")
    assert metadata
    assert metadata.dump(VIDEO_METADATA_TEST_DUMP_PATH)

    loaded_metadata = MextractorVideoMetadata.parse_file(path=VIDEO_METADATA_TEST_DUMP_PATH)
    assert loaded_metadata
