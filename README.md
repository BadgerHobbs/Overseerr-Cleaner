# Overseerr-Cleaner
Docker container and Python program to remove movies deleted form Plex from Overseerr

# Setup

## Build Docker Image
```bash
docker build -t overseerr-cleaner:latest .
```

## Run Docker Container
```bash
docker run -d \
    --name overseerr-cleaner \
    --restart unless-stopped \
    -e PLEX_TOKEN=XXXXX \                       # API token from Plex
    -e PLEX_HOST=XXXXX \                        # (Optional) Plex hostname (e.g. localhost)
    -e PLEX_PORT=XXXXX \                        # (Optional) Plex port (e.g. 32400)
    -e INTERVAL=XXXXX \                         # (Optional) Interval seconds
    -v /path/to/overseerr/db:/overseerr-db \    # Path to Overseerr database folder
    overseerr-cleaner:latest
```