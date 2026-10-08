from pathlib import Path

from mextractor.workflow import extract_and_dump_video
from tests import STATICS_PATH

extract_and_dump_video(dump_dir=Path("."), path_to_video=STATICS_PATH / "mouse_in_box.mp4", include_image=False)
