# IntegratedServer/server/routes/redirect_routes.py
# Redirect routes - /m/<shortId>, ad intermediate page
# Ported from Movieweb redirect logic

from flask import request, jsonify, redirect, render_template_string
from server.routes import redirect_bp
from database.supabase_client import supabase
from datetime import datetime, timedelta


def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


# --- Ad view session management ---

@redirect_bp.route('/api/check-ad/<short_id>', methods=['GET'])
def check_ad_viewed(short_id):
    """Check if user has already viewed ad for this short link"""
    try:
        ip = get_client_ip()
        link_type = request.args.get('type', 'single')

        rows = supabase.select('ad_view_sessions', '*', {
            'ip_address': ip,
            'short_id': short_id,
            'link_type': link_type
        })

        if rows:
            expires_at = rows[0].get('expires_at', '')
            if expires_at:
                # Check if session is still valid (5 minutes)
                try:
                    exp_time = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                    if exp_time > datetime.now(exp_time.tzinfo):
                        return jsonify({'adViewed': True, 'canSkip': True})
                except:
                    pass

        return jsonify({'adViewed': False, 'canSkip': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@redirect_bp.route('/api/record-ad-view', methods=['POST'])
def record_ad_view():
    """Record that user viewed the ad"""
    try:
        data = request.get_json()
        ip = get_client_ip()
        short_id = data.get('shortId', data.get('short_id', ''))
        link_type = data.get('linkType', data.get('link_type', 'single'))

        expires = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

        # Try to insert, ignore if duplicate
        try:
            supabase.insert('ad_view_sessions', {
                'ip_address': ip,
                'short_id': short_id,
                'link_type': link_type,
                'expires_at': expires
            })
        except:
            # Update existing
            supabase.update('ad_view_sessions', {
                'expires_at': expires,
                'viewed_at': datetime.utcnow().isoformat()
            }, {'ip_address': ip, 'short_id': short_id})

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Redirect endpoints ---

@redirect_bp.route('/m/<short_id>')
def movie_redirect(short_id):
    """Redirect for movies - shows ad page first, supports per-link short IDs"""
    try:
        import json as json_mod

        movie = None
        target_link = ''
        link_label = 'Download'

        # 1. Check main short_id field
        rows = supabase.select('movies', '*', {'short_id': short_id})
        if rows:
            movie = rows[0]
            dtype = movie.get('download_type', 'single')
            if dtype == 'single':
                target_link = movie.get('original_link', '')
            elif dtype == 'quality':
                target_link = movie.get('quality_720p') or movie.get('quality_480p') or movie.get('quality_1080p', '')
            else:
                target_link = movie.get('original_link', '')

        # 2. If not found, search short_ids JSON across all movies
        if not movie:
            all_movies = supabase.select('movies', '*')
            for m in all_movies:
                sids_raw = m.get('short_ids', '{}')
                try:
                    sids = json_mod.loads(sids_raw) if isinstance(sids_raw, str) else (sids_raw or {})
                except:
                    sids = {}
                for key, sid in sids.items():
                    if sid == short_id:
                        movie = m
                        # Resolve the actual link based on key
                        if key == 'original':
                            target_link = m.get('original_link', '')
                            link_label = 'Download'
                        elif key in ('480p', 'zip_480p'):
                            target_link = m.get('quality_480p', '')
                            link_label = '480p Download'
                        elif key in ('720p', 'zip_720p'):
                            target_link = m.get('quality_720p', '')
                            link_label = '720p Download'
                        elif key in ('1080p', 'zip_1080p'):
                            target_link = m.get('quality_1080p', '')
                            link_label = '1080p Download'
                        elif key.startswith('e') and '_' in key:
                            # Episode link e.g. e1_480p
                            ep_num, quality = key.split('_', 1)
                            link_label = f'{ep_num.upper()} {quality} Download'
                            try:
                                eps = json_mod.loads(m.get('episodes', '[]')) if isinstance(m.get('episodes'), str) else (m.get('episodes') or [])
                                ep_n = int(ep_num[1:])
                                for ep in eps:
                                    if ep.get('episodeNumber') == ep_n:
                                        target_link = ep.get(f'quality{quality}') or ep.get(f'quality{quality.capitalize()}', '')
                                        break
                            except:
                                pass
                        break
                if movie:
                    break

        if not movie:
            return "Movie not found", 404

        # Increment views
        supabase.update('movies', {'views': (movie.get('views', 0) or 0) + 1}, {'id': movie['id']})

        # If ads disabled, redirect directly
        if not movie.get('ads_enabled', True):
            if target_link:
                return redirect(target_link)

        # Show ad page with 10-second timer
        return render_template_string(AD_PAGE_TEMPLATE, movie=movie, short_id=short_id, target_link=target_link, link_label=link_label)
    except Exception as e:
        return f"Error: {e}", 500


@redirect_bp.route('/api/get-download/<short_id>')
def get_download_link(short_id):
    """Get the actual download link after ad viewing"""
    try:
        rows = supabase.select('movies', '*', {'short_id': short_id})
        if not rows:
            return jsonify({'error': 'Not found'}), 404

        movie = rows[0]
        dtype = movie.get('download_type', 'single')
        quality = request.args.get('quality', '')

        if dtype == 'single':
            link = movie.get('original_link', '')
        elif dtype == 'quality':
            if quality == '480p':
                link = movie.get('quality_480p', '')
            elif quality == '720p':
                link = movie.get('quality_720p', '')
            elif quality == '1080p':
                link = movie.get('quality_1080p', '')
            else:
                link = movie.get('quality_720p') or movie.get('quality_480p') or movie.get('quality_1080p', '')
        else:
            link = movie.get('original_link', '')

        return jsonify({'link': link, 'title': movie.get('title', '')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Ad page HTML template ---
AD_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ movie.title }} - Download</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: linear-gradient(135deg, #0a0e1a, #1a1040, #0f172a);
            color: #fff; min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }
        .container { text-align: center; padding: 2rem; max-width: 500px; width: 90%; }
        .movie-icon { font-size: 3rem; margin-bottom: 12px; }
        .title { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffd700; }
        .label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 1.5rem; }
        .timer-box {
            background: rgba(255,255,255,0.06); border-radius: 20px;
            padding: 2rem; margin: 1.5rem 0; backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .timer-text { font-size: 0.9rem; color: #94a3b8; }
        .timer { font-size: 5rem; font-weight: 700; color: #06b6d4; margin: 0.5rem 0;
                 text-shadow: 0 0 30px rgba(6,182,212,0.4); }
        .progress-bar {
            width: 100%; height: 6px; background: rgba(255,255,255,0.1);
            border-radius: 3px; overflow: hidden; margin: 1.2rem 0;
        }
        .progress-fill {
            height: 100%; background: linear-gradient(90deg, #06b6d4, #6366f1, #ffd700);
            border-radius: 3px; transition: width 1s linear; width: 0%;
        }
        .status-text { font-size: 0.8rem; color: #64748b; }
        .ad-space {
            margin: 1.5rem 0; padding: 1.5rem; min-height: 120px;
            background: rgba(255,255,255,0.03); border-radius: 14px;
            border: 1px dashed rgba(255,255,255,0.08);
            display: flex; align-items: center; justify-content: center;
            color: #475569; font-size: 0.85rem;
        }
        .download-btn {
            display: none; padding: 18px 56px; font-size: 1.1rem;
            background: linear-gradient(135deg, #06b6d4, #6366f1);
            color: #fff; border: none; border-radius: 14px;
            cursor: pointer; font-weight: 700; text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 8px 30px rgba(6,182,212,0.3);
        }
        .download-btn:hover { transform: scale(1.05); box-shadow: 0 12px 40px rgba(6,182,212,0.5); }
        .download-btn.show { display: inline-block; animation: bounceIn 0.6s; }
        @keyframes bounceIn {
            0% { opacity:0; transform:scale(0.3); }
            50% { transform:scale(1.05); }
            70% { transform:scale(0.95); }
            100% { opacity:1; transform:scale(1); }
        }
        .footer { margin-top: 2rem; font-size: 0.75rem; color: #334155; }
    </style>
</head>
<body>
    <div class="container">
        <div class="movie-icon">🎬</div>
        <h1 class="title">{{ movie.title }}</h1>
        <p class="label">{{ link_label }}</p>
        <div class="timer-box">
            <p class="timer-text">Your download will be ready in</p>
            <div class="timer" id="timer">10</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            <p class="status-text" id="statusText">⏳ Preparing your download link...</p>
        </div>
        <div class="ad-space" id="adSpace">
            Advertisement Space
        </div>
        <a href="{{ target_link }}" class="download-btn" id="downloadBtn">
            📥 {{ link_label }}
        </a>
        <p class="footer">MovieZone • Powered by MovieBot</p>
    </div>
    <script>
        let seconds = 10;
        const timer = document.getElementById('timer');
        const progress = document.getElementById('progress');
        const btn = document.getElementById('downloadBtn');
        const statusText = document.getElementById('statusText');

        const interval = setInterval(() => {
            seconds--;
            timer.textContent = seconds;
            progress.style.width = ((10 - seconds) / 10 * 100) + '%';
            if (seconds <= 5) statusText.textContent = '⚡ Almost there...';
            if (seconds <= 0) {
                clearInterval(interval);
                timer.textContent = '✅';
                statusText.textContent = '🎉 Your download is ready!';
                btn.classList.add('show');
                // Record ad view
                fetch('/api/record-ad-view', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({shortId: '{{ short_id }}'})
                });
            }
        }, 1000);
    </script>
</body>
</html>
"""

