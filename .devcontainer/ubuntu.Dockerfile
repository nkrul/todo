FROM docker.io/ubuntu:26.04
# https://github.com/nkrul/todo
# DEBUGGING: docker build -f .devcontainer/ubuntu.Dockerfile -t ubuntu-dev . && docker run -it ubuntu-dev bash
ARG USERNAME=ubuntu
ARG NAME=todo

# consider lscr.io/linuxserver/code-server:latest

# Locale stuff (use package, or can just inject)
# Use Locales
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
# Locale injector
# RUN \
    # echo LANGUAGE=en_US.UTF-8 >> /etc/environment && \
    # echo LC_ALL=en_US.UTF-8 >> /etc/environment && \
    # echo LANG=en_US.UTF-8 >> /etc/environment && \
    # echo LC_CTYPE=en_US.UTF-8 >> /etc/environment


RUN apt-get update && \
    apt-get -y install sudo wget curl vim git unzip && \
    rm -rf /var/lib/apt/lists/*

# # podman (instead of docker)
# RUN apt-get update && \
#     apt-get -y install podman podman-docker && \
#     rm -rf /var/lib/apt/lists/*

# Install libnss-mdns
RUN apt-get update && \
    apt-get -y install libnss-mdns && \
    rm -rf /var/lib/apt/lists/*
# Update nsswitch.conf to route .local queries through mdns
RUN sed -i 's/hosts:.*/hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4/' /etc/nsswitch.conf


# Android and Buildozer requirements
# Step 1: Install Java Development Kit (JDK) and any 'buildozer' required packages (like zlib)
RUN apt-get update && \
    apt-get -y install \
    openjdk-17-jdk  \
    build-essential autoconf automake libtool \
    zlib1g-dev libltdl-dev libmpdec-dev libssl-dev libffi-dev \
    && \
    rm -rf /var/lib/apt/lists/*
# GL/gl.h and SDL2 dependencies for Kivy
# RUN apt-get update && apt-get install -y \
#     libgl-dev \
#     libgles-dev \
#     libgl1-mesa-dev \
#     libgles2-mesa-dev \
#     libsdl2-dev \
#     libsdl2-image-dev \
#     libsdl2-mixer-dev \
#     libsdl2-ttf-dev \
#     libportmidi-dev \
#     libswscale-dev \
#     libavformat-dev \
#     libavcodec-dev \
#     && \
#     rm -rf /var/lib/apt/lists/*

# libglu1-mesa-dev

# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-dev \
#     libgles2-mesa-dev \
#     mesa-common-dev \
#     libglvnd-dev \
#     libsdl2-dev \
#     libsdl2-image-dev \
#     libsdl2-mixer-dev \
#     libsdl2-ttf-dev \
#     pkg-config \
#     && \
#     rm -rf /var/lib/apt/lists/*
# # Step 2: Set environment variables for Android SDK
# ENV ANDROID_SDK_ROOT=/opt/android-sdk
# ENV PATH=${PATH}:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools
# # Step 4: Download and extract Android Command Line Tools
# # Always verify the latest version identifier on the Android Developer website
# ARG CMD_LINE_FILE=commandlinetools-linux-14742923_latest.zip
# RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools && \
#     wget -q https://dl.google.com/android/repository/${CMD_LINE_FILE} -O /tmp/cmdline-tools.zip && \
#     unzip -q /tmp/cmdline-tools.zip -d /tmp && \
#     mv /tmp/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
#     rm /tmp/cmdline-tools.zip
# # # Step 5: Automatically accept SDK licenses
# RUN yes | sdkmanager --licenses
# # Step 6: Install required SDK components (Adjust versions as needed)
# # Except that sdkmanager is handled by the buildozer tool, so we don't need to do this manually.
# # RUN sdkmanager "platform-tools" \
# #                "platforms;android-33" \
# #                "build-tools;33.0.0"

# ARG GO_SRC_FILE=go1.24.5.linux-amd64.tar.gz
# RUN \
#     curl -OL https://go.dev/dl/${GO_SRC_FILE} && \
#     tar -C /usr/local -xf ${GO_SRC_FILE}
# ENV PATH="${PATH}:/usr/local/go/bin"
# ENV GOPRIVATE=*.kncept.com

# # protoc
# RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
#     DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes protobuf-compiler && \
#     rm -rf /var/lib/apt/lists/*

# ENV GOPATH=/home/${USERNAME}/go
# # export GOPATH=$HOME/gowork
# # export GOBIN=$GOPATH/bin  # sufficiently defaulted
# ENV PATH=$PATH:$GOPATH/bin
# # export PATH=$PATH:$GOPATH/bin
# # export GOROOT=/usr/local/go
# ENV GOROOT=/usr/local/go


# User
# RUN adduser ${USERNAME}
# RUN usermod -aG sudo ${USERNAME}
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN echo "${USERNAME}:${USERNAME}" | chpasswd
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# python stuff
# https://docs.astral.sh/uv/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN /home/${USERNAME}/.local/bin/uv python install 3.12 --default

# use the MANUALLY created .venv directory 
RUN printf "if [ -f /workspaces/${NAME}/.venv/bin/activate ]; then\n\tsource /workspaces/${NAME}/.venv/bin/activate\nfi\n" >> /home/${USERNAME}/.bashrc


# https://github.com/nvm-sh/nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
RUN /bin/bash -c ". .nvm/nvm.sh && nvm install --lts"

# Golang github 'insteadof' thingy
# RUN \
#     echo "[url \"ssh://git@github.com/\"]" >> .gitconfig && \
#     echo "        insteadOf = https://github.com/" >> .gitconfig

# # Golang Tools
# RUN go install golang.org/x/tools/gopls@v0.20.0
# RUN go install github.com/go-delve/delve/cmd/dlv@v1.25.1
# # RUN go install -v github.com/go-delve/delve/cmd/dlv@latest

# protoc tool?
#RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
# RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.6


# RUN curl -fsSL https://claude.ai/install.sh | bash


