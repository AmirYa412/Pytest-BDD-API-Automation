ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} python:3.14-slim

WORKDIR /app

# Dependencies first — this layer gets cached.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# pytest is always the entrypoint.
# Any args you pass to `docker run` get appended after it.
CMD ["pytest"]
