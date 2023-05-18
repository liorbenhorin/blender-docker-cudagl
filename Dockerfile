# Use Nvidia CUDA 11.4.2 base iamge
FROM nvidia/cudagl:11.4.2-base-ubuntu20.04

# Set environment vars
ENV DEBIAN_FRONTEND noninteractive
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_VISIBLE_DEVICES all

# Install Dependencies
RUN apt-get update && \
    apt-get install -y  \
    wget  \
    xz-utils  \
    curl  \
    unzip \
    libgl1-mesa-glx \
    libxi6 \
    libgconf-2-4 \
    libxcursor1 \
    libxss1 \
    libxrender1 \
    libxcomposite1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgtk-3-0 \
    libnss3 \
    libxkbcommon-x11-0 \
    libxslt1.1 \
    libx11-dev \
    libxxf86vm-dev \
    libxcursor-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libglew-dev \
    libsm6 \
    libxext6

# Install Blender 3.5.1
ENV BLENDER_ROOT "/opt/blender"
ENV BLENDER_VER  3.5

RUN wget -P /opt/blender https://download.blender.org/release/Blender3.5/blender-3.5.1-linux-x64.tar.xz && \
    mkdir -p $BLENDER_ROOT && \
    tar xvf "$BLENDER_ROOT/blender-3.5.1-linux-x64.tar.xz" -C $BLENDER_ROOT --strip-components 1

# Add blender to PATH
ENV PATH "$BLENDER_ROOT/$BLENDER_VER/python/bin:$PATH"
ENV PATH "$BLENDER_ROOT:$PATH"

ENTRYPOINT ["blender"]


