# mextractor: media metadata extractor

Videos and images can be large. 

## Installation

Download and install from PyPi with `pip`:

```shell
pip install mextractor
```

## Usage

### Extract and dump metadata
```python
import mextractor

metadata = mextractor.extract_and_dump(path_to_dump, path_to_media)
```

### Load media

#### Video

```python
import mextractor

video_metadata = mextractor.parse_file(path_to_metadata)

print(video_metadata.fps)
print(video_metadata.frames)
print(video_metadata.resolution)
print(video_metadata.seconds)
print(video_metadata.path)
print(video_metadata.bytes)
```

#### Image

```python
import mextractor

image_metadata = mextractor.parse_file(path_to_metadata)

print(image_metadata.resolution)
print(image_metadata.path)
print(image_metadata.bytes)
```
