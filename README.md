# mextractor: media metadata extractor

Videos and images can be large. 

## Installation

Download and install from PyPi with `pip`:

```shell
pip install mextractor
```
If you are extracting metadata from videos, install additional dependencies:
```shell
pip install mextractor[video-extract]
```

## Usage
Please back up your files before using them with the package, things might break during runtime causing corruption.

### Command line interface (CLI)

Copy directory to a new directory while extracting media info and a single frame from videos in subdirectories:
```shell
mextractor video-subdirs <path_to_root>
```

### Programmatically
These functions are useful when integrating mextractor to your own package. You can also use it for quick scripts, see the `mextractor.workflows` submodule for inspiration.

#### Extract and dump metadata

##### Video

```python
from mextractor.workflow import extract_and_dump_video

metadata = extract_and_dump_video(dump_dir, path_to_video, include_image, greyscale, lossy_compress_image)
```

##### Image

```python
from mextractor.workflow import extract_and_dump_image

metadata = extract_and_dump_image(dump_dir, path_to_image, include_image, greyscale, lossy_compress_image)
```

#### Load media

##### Video

```python
import mextractor

video_metadata = mextractor.load(mextractor_dir)

print(video_metadata.average_fps)
print(video_metadata.frames)
print(video_metadata.resolution)
print(video_metadata.video_length_in_seconds)
```

##### Image

```python
import mextractor

image_metadata = mextractor.load(mextractor_dir)

print(image_metadata.resolution)
```
