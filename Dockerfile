# Official multi-arch Python image (works on both ARM64 and x86_64)
FROM python:3.13-slim

# System libraries: Pango for weasyprint (HTML to PDF), Poppler for pdf2image
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    fonts-dejavu-core \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# Install Python packages (TA-Lib ships prebuilt wheels, so no C build step is needed)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
