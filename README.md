# mextractor: media metadata extractor

Videos and images are large; sometimes, I only need the metadata of the media. `mextractor` automates the extraction and reading of these metadata files.

## Installation

Download and install from PyPi with `pip`:

```shell
pip install mextractor
```

## Usage

### Video

#### Extract
```python
import mextractor

metadata = mextractor.extract_video(path_to_video)
metadata.dump(path_to_metadata)
```

#### Load

```python
import mextractor

video_metadata = mextractor.parse_file(path_to_metadata)

print(video_metadata.fps)
print(video_metadata.frames)
print(video_metadata.resolution)
print(video_metadata.seconds)
print(video_metadata.milliseconds)
print(video_metadata.path)
print(video_metadata.bytes)
```

### Image

#### Extract
```python
import mextractor

metadata = mextractor.extract_image(path_to_image)
metadata.dump(path_to_metadata)
```

#### Load

```python
import mextractor
image_metadata = mextractor.parse_file(path_to_metadata)

print(image_metadata.resolution)
print(image_metadata.path)
print(image_metadata.bytes)
```
