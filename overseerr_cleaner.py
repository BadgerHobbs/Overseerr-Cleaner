from plexapi.myplex import PlexServer
import time
import sqlite3
import os

# Get docker environment variables
plex_token = os.getenv("PLEX_TOKEN")
plex_host = os.getenv("PLEX_HOST")
plex_port = int(os.getenv("PLEX_PORT", 0))
interval = int(os.getenv("INTERVAL", 0))

if not plex_token:
    print("Missing 'PLEX_TOKEN'")
    exit(1)

if not interval:
    print("Missing 'INTERVAL', defaulting to 24 hours")
    interval = 60 * 60 * 24

if not plex_host:
    print("Missing 'PLEX_HOST', defaulting to localhost")
    plex_host = "localhost"

if not plex_port:
    print("Missing 'PLEX_PORT', defaulting to 32400")
    plex_port = "32400"

print("Settings (Environment Variables):")
print(f"PLEX_TOKEN: {plex_token}")
print(f"PLEX_HOST: {plex_host}")
print(f"PLEX_PORT: {plex_port}")
print(f"INTERVAL: {interval}")

print("Running Overseerr cleaner...")

while True:
    
    # Connect to plex server
    plex = PlexServer(
        f"http://{plex_host}:{plex_port}", 
        plex_token,
    )
    
    # Get all plex content
    pelx_guid_lookup = {}
    for item in plex.library.all():
        try:
            pelx_guid_lookup[item.guid] = item
            pelx_guid_lookup.update({guid.id: item for guid in item.guids})
        except Exception as e:
            print(f"Error: {e}")
            pass

    # Connect to Overseerr Database
    conn = sqlite3.connect("overseerr-db/db.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT tmdbId FROM media")
    overseerr_content = [x[0] for x in cur.fetchall() if len(x) > 0]

    for overseerr_item in overseerr_content:

        plex_item = pelx_guid_lookup.get(f"tmdb://{overseerr_item}")
        
        if plex_item:
            print(f"Found: {overseerr_item}")
        else:
            print(f"Missing: {overseerr_item}")

            sql = f"UPDATE media SET mediaAddedAt = NULL, status = 1 WHERE tmdbId = ?"
            cur.execute(sql, [overseerr_item])
            conn.commit()

    conn.close()

    print("Waiting", interval, "seconds...")
    time.sleep(interval)