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
    python3.12 python3.12-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.12 - \
    && echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN export PATH=$HOME/.local/bin:$PATH && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python3.12", "manage.py", "runserver", "0.0.0.0:8000"]

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]