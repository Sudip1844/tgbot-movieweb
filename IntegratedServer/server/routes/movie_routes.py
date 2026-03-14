# IntegratedServer/server/routes/movie_routes.py
# Movie CRUD routes - ported from Movieweb/server/routes.ts
# NO API token system - direct access since same server

import secrets
from flask import request, jsonify
from server.routes import movie_bp
from database.supabase_client import supabase


def generate_short_id():
    return secrets.token_hex(3)  # 6-char hex


# --- Movie Links (single) ---

@movie_bp.route('/api/movie-links', methods=['GET'])
def get_movie_links():
    """Get all movies (approved only by default, ?all=true for everything)"""
    try:
        show_all = request.args.get('all', 'false').lower() == 'true'
        if show_all:
            movies = supabase.select('movies', '*', order='created_at.desc')
        else:
            movies = supabase.select('movies', '*', {'status': 'approved'}, order='created_at.desc')
        return jsonify(movies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movie-links', methods=['POST'])
def create_movie_link():
    """Create a new movie (from website admin panel) - generates per-link short URLs"""
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        dtype = data.get('downloadType', data.get('download_type', 'single'))
        short_id = generate_short_id()  # main short_id for backwards compat

        # Generate per-link short IDs
        short_ids = {}
        short_urls = {}
        host = request.host_url.rstrip('/')

        if dtype == 'single':
            sid = generate_short_id()
            short_ids['original'] = sid
            short_urls['original'] = f"{host}/m/{sid}"
        elif dtype == 'quality':
            for q in ['480p', '720p', '1080p']:
                key = f'quality{q}'
                camel = f'quality_{q}'
                if data.get(key) or data.get(camel):
                    sid = generate_short_id()
                    short_ids[q] = sid
                    short_urls[q] = f"{host}/m/{sid}"
        elif dtype == 'zip':
            for q in ['480p', '720p', '1080p']:
                key = f'quality{q}'
                camel = f'quality_{q}'
                if data.get(key) or data.get(camel):
                    sid = generate_short_id()
                    short_ids[f'zip_{q}'] = sid
                    short_urls[f'zip_{q}'] = f"{host}/m/{sid}"
        elif dtype == 'episode':
            # Episodes get short IDs per episode per quality
            episodes_data = data.get('episodes')
            if episodes_data:
                import json
                eps = json.loads(episodes_data) if isinstance(episodes_data, str) else episodes_data
                for ep in eps:
                    ep_num = ep.get('episodeNumber', 1)
                    for q in ['480p', '720p', '1080p']:
                        qkey = f'quality{q.capitalize()}' if q != '480p' else 'quality480p'
                        if ep.get(qkey) or ep.get(f'quality{q}'):
                            sid = generate_short_id()
                            short_ids[f'e{ep_num}_{q}'] = sid
                            short_urls[f'e{ep_num}_{q}'] = f"{host}/m/{sid}"

        import json as json_mod
        insert_data = {
            'title': data.get('title', data.get('movieName', data.get('movie_name', ''))),
            'original_link': data.get('originalLink', data.get('original_link', '')),
            'short_id': short_id,
            'short_ids': json_mod.dumps(short_ids),
            'download_type': dtype,
            'quality_480p': data.get('quality480p', data.get('quality_480p')),
            'quality_720p': data.get('quality720p', data.get('quality_720p')),
            'quality_1080p': data.get('quality1080p', data.get('quality_1080p')),
            'categories': data.get('categories', []),
            'languages': data.get('languages', []),
            'release_year': data.get('releaseYear', data.get('release_year', 'N/A')),
            'runtime': data.get('runtime', 'N/A'),
            'imdb_rating': data.get('imdbRating', data.get('imdb_rating', 'N/A')),
            'ads_enabled': data.get('adsEnabled', data.get('ads_enabled', True)),
            'status': data.get('status', 'pending'),
            'added_by': data.get('addedBy', data.get('added_by', 'owner')),
        }

        # Handle episodes
        if data.get('episodes'):
            insert_data['episodes'] = data['episodes']
            insert_data['download_type'] = 'episode'
            insert_data['start_from_episode'] = data.get('startFromEpisode', 1)

        # Handle zip
        if data.get('fromEpisode') is not None:
            insert_data['from_episode'] = data['fromEpisode']
            insert_data['to_episode'] = data.get('toEpisode')
            insert_data['download_type'] = 'zip'

        result = None
        try:
            result = supabase.insert('movies', insert_data)
        except Exception:
            # short_ids column might not exist yet, try without it
            insert_data.pop('short_ids', None)
            result = supabase.insert('movies', insert_data)

        if result:
            return jsonify({
                'success': True,
                'shortId': short_id,
                'shortIds': short_ids,
                'shortUrls': short_urls,
                'shortUrl': f"{host}/m/{short_id}",
                'id': result.get('id'),
                'movie': result
            }), 201

        return jsonify({'error': 'Failed to create'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movie-links/<short_id>', methods=['GET'])
def get_movie_link(short_id):
    """Get movie by short ID"""
    try:
        rows = supabase.select('movies', '*', {'short_id': short_id})
        if not rows:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(rows[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movie-links/<int:movie_id>', methods=['PATCH'])
def update_movie_link(movie_id):
    """Update a movie"""
    try:
        data = request.get_json()
        update_data = {}
        field_map = {
            'originalLink': 'original_link',
            'adsEnabled': 'ads_enabled',
            'title': 'title',
            'original_link': 'original_link',
            'ads_enabled': 'ads_enabled',
            'quality_480p': 'quality_480p',
            'quality_720p': 'quality_720p',
            'quality_1080p': 'quality_1080p',
            'categories': 'categories',
            'languages': 'languages',
            'status': 'status',
        }
        for key, db_key in field_map.items():
            if key in data:
                update_data[db_key] = data[key]

        if not update_data:
            return jsonify({'error': 'No update data'}), 400

        result = supabase.update('movies', update_data, {'id': movie_id})
        return jsonify(result or {'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movie-links/<short_id>/views', methods=['PATCH'])
def update_views(short_id):
    """Increment views"""
    try:
        rows = supabase.select('movies', 'id,views', {'short_id': short_id})
        if rows:
            supabase.update('movies', {'views': (rows[0].get('views', 0) or 0) + 1}, {'id': rows[0]['id']})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movie-links/<int:movie_id>', methods=['DELETE'])
def delete_movie_link(movie_id):
    """Delete a movie"""
    try:
        supabase.delete('movies', {'id': movie_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Review Queue ---

@movie_bp.route('/api/pending-movies', methods=['GET'])
def get_pending_movies():
    """Get movies pending review"""
    try:
        movies = supabase.select('movies', '*', {'status': 'pending'}, order='created_at.desc')
        return jsonify(movies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movies/<int:movie_id>/approve', methods=['POST'])
def approve_movie(movie_id):
    """Approve a movie"""
    try:
        supabase.update('movies', {'status': 'approved'}, {'id': movie_id})
        return jsonify({'success': True, 'message': 'Movie approved'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movie_bp.route('/api/movies/<int:movie_id>/reject', methods=['POST'])
def reject_movie(movie_id):
    """Reject a movie"""
    try:
        supabase.update('movies', {'status': 'rejected'}, {'id': movie_id})
        return jsonify({'success': True, 'message': 'Movie rejected'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
