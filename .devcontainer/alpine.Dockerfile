FROM alpine:3.22

## Current state - attempt to fix dns resolver for *.local

# https://github.com/nkrul/todo
# DEBUGGING: docker build -f .devcontainer/alpine.Dockerfile -t alpine-dev . && docker run -it alpine-dev sh
ARG USERNAME=todo

# RUN apk update
RUN apk add --no-cache shadow sudo git curl bash

# Install Avahi and the avahi2dns resolver package
RUN apk add --no-cache avahi avahi-tools avahi2dns
# Configure Alpine to use the local avahi2dns service (running on port 53)
RUN echo "nameserver 127.0.0.1" > /etc/resolv.conf

ARG GO_SRC_FILE=go1.24.5.linux-amd64.tar.gz
RUN curl -OL https://go.dev/dl/${GO_SRC_FILE} && \
    tar -C /usr/local -xf ${GO_SRC_FILE}
ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPRIVATE=*.kncept.com,github.com/kncept/*
ENV GOPATH=/home/${USERNAME}/go
ENV PATH=$PATH:$GOPATH/bin
ENV GOROOT=/usr/local/go

# prerequisites for nvm from https://github.com/nvm-sh/nvm?tab=readme-ov-file#alpine-linux-313
# RUN apk add --no-cache -U curl bash ca-certificates openssl ncurses coreutils python3 make gcc g++ libgcc linux-headers grep util-linux binutils findutils
RUN apk add --no-cache nodejs-lts npm

RUN addgroup -g 1000 ${USERNAME} \
    && adduser -u 1000 -G ${USERNAME} -G wheel -D ${USERNAME} \
    && usermod -g ${USERNAME} ${USERNAME}
RUN echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers
RUN echo "${USERNAME}:${USERNAME}" | chpasswd
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# python stuff
# https://docs.astral.sh/uv/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN /home/${USERNAME}/.local/bin/uv python install 3.13 --default

# use the MANUALLY created .venv directory 
RUN printf "if [ -f /workspaces/${USERNAME}/.venv/bin/activate ]; then\n\tsource /workspaces/${USERNAME}/.venv/bin/activate\nfi\n" >> /home/${USERNAME}/.profile


# THIS... seems to hang :(
# https://github.com/nvm-sh/nvm
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# RUN /bin/bash -c ". .nvm/nvm.sh && nvm install --lts"

# Golang github 'insteadof' thingy
RUN \
    echo "[url \"ssh://git@github.com/\"]" >> .gitconfig && \
    echo "        insteadOf = https://github.com/" >> .gitconfig

# Golang Tools
RUN go install golang.org/x/tools/gopls@v0.20.0
RUN go install github.com/go-delve/delve/cmd/dlv@v1.25.1
# RUN go install -v github.com/go-delve/delve/cmd/dlv@latest


# Install claude over LocalAI 
# This is a _really_ bad way to handle keys
# ENV ANTHROPIC_BASE_URL=http://192.168.0.19:8080
# ENV ANTHROPIC_API_KEY=todo55API
# ANTHROPIC_AUTH_TOKEN=todo55API
# ANTHROPIC_API_KEY=
# this is actually run via `claude --mode ${CLAUDE_MODEL}
# ENV CLAUDE_MODEL=gemma-4-12b-coder-fable5-composer2.5-v1

# RUN curl -fsSL https://claude.ai/install.sh | bash

# makd sure the dns resolver is run
CMD avahi-daemon --no-drop-root & avahi2dns --port 53 & wait