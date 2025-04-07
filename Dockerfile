FROM ubuntu:22.04

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies including Rust/Cargo
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    build-essential \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app
COPY . /app
RUN pip3 install uv
RUN uv pip install -r requirements.txt --system