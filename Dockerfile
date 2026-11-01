FROM python:3.12-slim

# The project has no Python dependencies. tzdata provides the Pacific time zone for quota resets.
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY idea_factory ./idea_factory
COPY migrations ./migrations
COPY web ./web

RUN useradd --system --no-create-home idea_factory
USER idea_factory

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "idea_factory", "run"]
