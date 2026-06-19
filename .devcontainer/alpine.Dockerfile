FROM alpine:3.22
# https://github.com/kncept/Refuel
# DEBUGGING: docker build -f .devcontainer/alpine.Dockerfile -t alpine-dev . && docker run -it alpine-dev sh
ARG USERNAME=todo

# RUN apk update
RUN apk add --no-cache shadow sudo git curl bash

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

