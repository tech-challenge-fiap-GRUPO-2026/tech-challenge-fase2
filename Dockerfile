FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    # Driver de video dummy: permite rodar pygame sem display (headless)
    SDL_VIDEODRIVER=dummy \
    SDL_AUDIODRIVER=dummy

WORKDIR /app

# Dependencias necessarias para pygame e o matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsdl2-2.0-0 \
        libsdl2-image-2.0-0 \
        libsdl2-mixer-2.0-0 \
        libsdl2-ttf-2.0-0 \
        libfreetype6 \
        libpng16-16 \
        libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias Python primeiro para aproveitar cache de camadas
COPY requirements.txt requirements-llm.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -r requirements-llm.txt

# Copia o código fonte
COPY . .

# Comando padrao: executa os experimentos VRP e gera artefatos
CMD ["python", "-m", "src.metrics", \
     "--deliveries-file", "data/deliveries_sample.csv", \
     "--vehicles-file", "data/vehicles_sample.csv", \
     "--output-dir", "artifacts"]
