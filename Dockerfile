FROM python:3.11-slim


EXPOSE 8501


RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
