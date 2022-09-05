# mextractor: media metadata extractor

Videos and images can be large. 

## Installation

Download and install from PyPi with `pip`:

```shell
pip install mextractor
```

## Usage

### Extract and dump metadata

#### Video

```python
from mextractor.workflow import extract_and_dump_video

metadata = extract_and_dump_video(dump_dir, path_to_video, include_image, greyscale, lossy_compress_image)
```

#### Image

```python
from mextractor.workflow import extract_and_dump_image

metadata = extract_and_dump_image(dump_dir, path_to_image, include_image, greyscale, lossy_compress_image)
```

### Load media

#### Video

```python
import mextractor

video_metadata = mextractor.load(mextractor_dir)

print(video_metadata.average_fps)
print(video_metadata.frames)
print(video_metadata.resolution)
print(video_metadata.video_length_in_seconds)
```

#### Image

```python
import mextractor

image_metadata = mextractor.load(mextractor_dir)

print(image_metadata.resolution)
```
