# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

FROM node:22-bookworm-slim

ARG CODEX_VERSION

RUN test -n "$CODEX_VERSION" \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        file \
        gh \
        git \
        git-lfs \
        jq \
        tar \
        unzip \
        wget \
    && npm install --global "@openai/codex@${CODEX_VERSION}" \
    && mkdir -p /root/.codex \
    && rm -rf /var/lib/apt/lists/* /root/.npm

WORKDIR /workspace

ENTRYPOINT ["codex"]
