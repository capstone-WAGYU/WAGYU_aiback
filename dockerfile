FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    build-essential cmake git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# llama-cpp-python을 cuBLAS로 빌드
ENV CMAKE_ARGS="-DGGML_CUDA=on" \
    FORCE_CMAKE=1

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000
CMD ["uvicorn", "main:APP", "--host", "0.0.0.0", "--port", "8000"]