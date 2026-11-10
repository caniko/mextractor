# mextractor vision

mextractor is a media metadata extractor for Python. It reads videos and images,
produces typed metadata (optionally with a single representative frame), dumps
that metadata to YAML, and reads it back later. Its CLI workflow copies a
directory tree while extracting metadata and one frame per video, so an
analysis project can work from a small, portable description of a large media
collection instead of the collection itself.

## Problem

Video and image files are large, and the facts needed to analyse them — size,
duration, frame count, codec, a thumbnail — are small. Every project that needs
those facts writes its own OpenCV/ffmpeg loop, writes the results in an ad hoc
format, and then writes a second parser to load them. The duplication is dull
and the formats drift between projects.

## Principles

- **Copy, never convert in place.** The documented workflow copies to a new
  directory and extracts alongside; the README warns users to back up their
  files because runtime failures can corrupt media input.
- **Metadata round-trips.** Extraction dumps YAML and the same models load it
  back, so downstream code reads one representation.
- **Video support is optional.** Frame and video dependencies live behind the
  `video-extract` extra; image-only work stays light.
- **One code path for images and videos.** A merged media model keeps the
  workflow shared, with separate dumps only where the fields differ.
- **Typed output.** Pydantic models and NumPy arrays describe the extracted
  data rather than nested dictionaries.

## Scope

- metadata extraction for videos and images
- optional single-frame extraction and lossy image compression
- YAML dump and load
- `extract` CLI command that copies a tree and extracts media info
- workflow helpers for integrating extraction into another package
- packaging as a PyPI project with a uv-locked development environment

## Direction

The unreleased changelog is packaging and dependency maintenance: PEP 621
metadata with uv locking, headless OpenCV, and NumPy's array annotation with
current pydantic-numpy.

## Place in the fleet

`oul-analysis` depends on `mextractor>=6.0.2,<7` and pins a git revision in its
`pyproject.toml`.
