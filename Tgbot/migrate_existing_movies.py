#!/usr/bin/env python3
"""
Migration script to add existing movies to monthly statistics tracking
"""

import json
import os
from datetime import datetime
import database as db

def migrate_existing_movies():
    """Migrate existing movies to monthly stats tracking."""
    try:
        # Load existing movies
        movies_data = db.load_json(db.MOVIES_FILE)
        
        print(f"Found {len(movies_data['movies'])} existing movies")
        
        for movie_id_str, movie_data in movies_data['movies'].items():
            movie_id = int(movie_id_str)
            
            # Extract added_at date
            added_at = movie_data.get('added_at')
            if not added_at:
                print(f"Skipping movie {movie_id} - no added_at date")
                continue
            
            # Parse date to get year and month
            try:
                if 'T' in added_at:
                    # ISO format: 2025-08-08T16:50:38.577680
                    date_obj = datetime.fromisoformat(added_at.replace('Z', '+00:00'))
                else:
                    # Try other formats
                    date_obj = datetime.fromisoformat(added_at)
                
                print(f"Processing movie '{movie_data.get('title', 'Unknown')}' added on {date_obj.strftime('%Y-%m-%d')}")
                
                # Track this movie addition manually
                db.track_movie_addition_for_date(movie_id, movie_data, date_obj)
                
                # If movie has downloads, track them for current month
                download_count = movie_data.get('download_count', 0)
                if download_count > 0:
                    print(f"  Adding {download_count} downloads for current month")
                    for _ in range(download_count):
                        db.track_movie_download(movie_id)
                        
            except Exception as e:
                print(f"Error processing movie {movie_id}: {e}")
                continue
        
        print("Migration completed!")
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_existing_movies()