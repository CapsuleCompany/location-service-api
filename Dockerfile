# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables to make tzdata non-interactive
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Add Deadsnakes PPA for Python 3.12
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update

# Install prerequisites and Python 3.12
RUN apt-get install -y \
    wget build-essential curl unzip pkg-config \
    libdbus-1-dev dbus dbus-x11 libgirepository1.0-dev gobject-introspection \
    libcairo2-dev libjpeg-dev libpng-dev libffi-dev \
    gdal-bin libgdal-dev libgeos-dev \
    python3.12 python3.12-dev python3.12-venv libpq-dev \
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

# Copy application code and requirements file
COPY . /app/

# Install Python dependencies globally
RUN python3.12 -m pip install --upgrade pip setuptools wheel \
    && python3.12 -m pip install --no-cache-dir -r requirements.txt \
    && python3.12 -m pip install --no-cache-dir kafka-python-ng six

# Expose port
EXPOSE 8000

# Run the application
CMD ["python3.12", "manage.py", "runserver", "0.0.0.0:8000"]

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]