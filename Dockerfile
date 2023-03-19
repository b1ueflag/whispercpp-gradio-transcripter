# Dockerfile
FROM python:3.9

# Set working directory
WORKDIR /app

# Set the timezone
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    libasound2-dev \
    ffmpeg

# Clone the whisper repository
RUN git clone https://github.com/ggerganov/whisper.cpp.git

# Build whisper binary
RUN cd whisper.cpp && \
    bash ./models/download-ggml-model.sh base && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make

# Install Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY app.py .

# Set Gradio server name
ENV GRADIO_SERVER_NAME=0.0.0.0

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
