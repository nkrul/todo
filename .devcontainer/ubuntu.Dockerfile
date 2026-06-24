FROM docker.io/ubuntu:26.04
# https://github.com/nkrul/todo
# DEBUGGING: docker build -f .devcontainer/ubuntu.Dockerfile -t ubuntu-dev . && docker run -it ubuntu-dev bash
ARG USERNAME=ubuntu
ARG NAME=todo

# consider lscr.io/linuxserver/code-server:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y locales && \
    locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install sudo wget curl vim git && \
    rm -rf /var/lib/apt/lists/*

# Install libnss-mdns
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install libnss-mdns && \
    rm -rf /var/lib/apt/lists/*
# Update nsswitch.conf to route .local queries through mdns
RUN sed -i 's/hosts:.*/hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4/' /etc/nsswitch.conf


# Locale injector
# RUN \
    # echo LANGUAGE=en_US.UTF-8 >> /etc/environment && \
    # echo LC_ALL=en_US.UTF-8 >> /etc/environment && \
    # echo LANG=en_US.UTF-8 >> /etc/environment && \
    # echo LC_CTYPE=en_US.UTF-8 >> /etc/environment

ARG GO_SRC_FILE=go1.24.5.linux-amd64.tar.gz
RUN \
    curl -OL https://go.dev/dl/${GO_SRC_FILE} && \
    tar -C /usr/local -xf ${GO_SRC_FILE}
ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPRIVATE=*.kncept.com

# protoc
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes protobuf-compiler && \
    rm -rf /var/lib/apt/lists/*

ENV GOPATH=/home/${USERNAME}/go
# export GOPATH=$HOME/gowork
# export GOBIN=$GOPATH/bin  # sufficiently defaulted
ENV PATH=$PATH:$GOPATH/bin
# export PATH=$PATH:$GOPATH/bin
# export GOROOT=/usr/local/go
ENV GOROOT=/usr/local/go


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
RUN /home/${USERNAME}/.local/bin/uv python install 3.13 --default

# use the MANUALLY created .venv directory 
RUN printf "if [ -f /workspaces/${NAME}/.venv/bin/activate ]; then\n\tsource /workspaces/${USERNAME}/.venv/bin/activate\nfi\n" >> /home/${USERNAME}/.profile


# https://github.com/nvm-sh/nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
RUN /bin/bash -c ". .nvm/nvm.sh && nvm install --lts"

# Golang github 'insteadof' thingy
RUN \
    echo "[url \"ssh://git@github.com/\"]" >> .gitconfig && \
    echo "        insteadOf = https://github.com/" >> .gitconfig

# Golang Tools
RUN go install golang.org/x/tools/gopls@v0.20.0
RUN go install github.com/go-delve/delve/cmd/dlv@v1.25.1
# RUN go install -v github.com/go-delve/delve/cmd/dlv@latest

# protoc tool?
#RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
# RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.6


# RUN curl -fsSL https://claude.ai/install.sh | bash


