# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables to make tzdata non-interactive
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install prerequisites
RUN apt-get update && apt-get install -y \
    software-properties-common wget build-essential curl unzip pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12 manually
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && apt-get install -y \
    python3.12 python3.12-dev python3.12-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install GDAL and dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin libgdal-dev libgeos-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Cairo dependencies for pycairo
RUN apt-get update && apt-get install -y \
    libcairo2-dev libjpeg-dev libpng-dev libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Manually install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.12 get-pip.py && rm get-pip.py

# Set up aliases for convenience
RUN echo "alias python=python3.12" >> ~/.bashrc && \
    echo "alias makemigrations='python manage.py makemigrations'" >> ~/.bashrc && \
    echo "alias migrate='python manage.py migrate'" >> ~/.bashrc

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app/

# Install Python dependencies
RUN python3.12 -m pip install --upgrade pip \
    && python3.12 -m pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the application without using the virtual environment
CMD ["python3.12", "manage.py", "runserver", "0.0.0.0:8000"]

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]
