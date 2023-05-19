# Blender Docker + CUDA Support for Windows / Linux 🪟🐧

This can be used for testing automations that are designated to run on a cloud environment,
or simply as a reliable form of rendering / batching of blender files, with no concerns of contamination from the local environment. 

## Requirements

- Docker installed + GPU enabled
- Latest Nvidia Drivers
- RTX GPU

### Note
Windows dockers run using WSL will have no Optix support.
This is not yet supported by Nvidia

## Quickstart

You can pull the already built image from my dockerhub and start using it immediately.

The image entrypoint is blender's executable, as demonstrated below

```shell
docker run -it --gpus=all --rm liorbenhorin/blender35:latest <pass your blender commands here, eg. --background>
```

## To build a local container

```shell
dokcer build -t blender35:latest .

```

## Test
```shell
docker run -it --gpus=all --rm -v .:/tests blender35:latest --background --python /tests/render_test.py --log-level -1 -d --debug-cycles --debug-gpu
```