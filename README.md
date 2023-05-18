# Blender Docker + CUDA Support for Windows / Linux 🪟🐧

## Requirements

- Docker installed + GPU enabled
- Latest Nvidia Drivers
- RTX GPU

### Note
Windows dockers run using WSL will have no Optix support.
This is not yet supported by Nvidia

## Quickstart


```shell
docker run -it --gpus=all --rm liorbenhorin/blender35:latest <pass your blender commands here, eg. --background>
```




