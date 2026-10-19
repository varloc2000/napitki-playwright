FROM mcr.microsoft.com/playwright:v1.64.0-noble

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
# Pin playwright to the image tag so bundled browsers match
RUN pip3 install --no-cache-dir --break-system-packages fastapi uvicorn playwright==1.64.0

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
