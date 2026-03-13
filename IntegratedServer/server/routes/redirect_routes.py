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
    """Redirect for single/quality movies - shows ad page first"""
    try:
        rows = supabase.select('movies', '*', {'short_id': short_id})
        if not rows:
            return "Movie not found", 404

        movie = rows[0]

        # Increment views
        supabase.update('movies', {'views': (movie.get('views', 0) or 0) + 1}, {'id': movie['id']})

        # If ads disabled, redirect directly
        if not movie.get('ads_enabled', True):
            target = movie.get('original_link', '')
            if target:
                return redirect(target)

        # Show ad page with 10-second timer
        return render_template_string(AD_PAGE_TEMPLATE, movie=movie, short_id=short_id)
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
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff; min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }
        .container {
            text-align: center; padding: 2rem;
            max-width: 500px; width: 90%;
        }
        .title { font-size: 1.5rem; margin-bottom: 1rem; color: #ffd700; }
        .timer-box {
            background: rgba(255,255,255,0.1); border-radius: 16px;
            padding: 2rem; margin: 1.5rem 0; backdrop-filter: blur(10px);
        }
        .timer {
            font-size: 4rem; font-weight: bold;
            color: #00d2ff; margin: 1rem 0;
        }
        .progress-bar {
            width: 100%; height: 6px; background: rgba(255,255,255,0.2);
            border-radius: 3px; overflow: hidden; margin: 1rem 0;
        }
        .progress-fill {
            height: 100%; background: linear-gradient(90deg, #00d2ff, #ffd700);
            border-radius: 3px; transition: width 1s linear; width: 0%;
        }
        .download-btn {
            display: none; padding: 16px 48px; font-size: 1.2rem;
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            color: #fff; border: none; border-radius: 12px;
            cursor: pointer; font-weight: bold; text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .download-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0,210,255,0.4);
        }
        .download-btn.show { display: inline-block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
        .ad-space {
            margin: 1.5rem 0; padding: 1rem;
            background: rgba(255,255,255,0.05); border-radius: 8px;
            min-height: 100px;
        }
        .info { color: #aaa; font-size: 0.9rem; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">🎬 {{ movie.title }}</h1>
        <div class="timer-box">
            <p>Your download will be ready in</p>
            <div class="timer" id="timer">10</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            <p class="info">Please wait while we prepare your download link...</p>
        </div>
        <div class="ad-space" id="adSpace">
            <!-- Ad space -->
        </div>
        <a href="#" class="download-btn" id="downloadBtn" onclick="startDownload()">
            📥 Download Now
        </a>
    </div>
    <script>
        let seconds = 10;
        const timer = document.getElementById('timer');
        const progress = document.getElementById('progress');
        const btn = document.getElementById('downloadBtn');

        const interval = setInterval(() => {
            seconds--;
            timer.textContent = seconds;
            progress.style.width = ((10 - seconds) / 10 * 100) + '%';
            if (seconds <= 0) {
                clearInterval(interval);
                timer.textContent = '✅';
                btn.classList.add('show');
                // Record ad view
                fetch('/api/record-ad-view', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({shortId: '{{ short_id }}'})
                });
            }
        }, 1000);

        function startDownload() {
            fetch('/api/get-download/{{ short_id }}')
                .then(r => r.json())
                .then(data => {
                    if (data.link) window.location.href = data.link;
                    else alert('Download link not available');
                });
        }
    </script>
</body>
</html>
"""
