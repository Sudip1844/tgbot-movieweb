# IntegratedServer/server/app.py
# Flask Application Setup

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import logging
from typing import Union
from config import Config, ALLOWED_ORIGINS, API_PREFIX
from database import init_db

logger = logging.getLogger(__name__)

def create_app():
    """Flask application factory"""
    app = Flask(__name__, static_folder='../static')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize Database
    logger.info("Initializing database...")
    init_db()
    
    # Setup CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # Register middleware
    register_middleware(app)
    
    # Register routes
    register_routes(app)
    
    logger.info(f"✅ Flask app created and configured")
    return app

def register_middleware(app: Flask) -> None:
    """Register request/response middleware"""
    
    @app.before_request
    def before_request() -> None:
        """Log incoming requests"""
        logger.info(f"{request.method} {request.path}")
    
    @app.after_request
    def after_request(response: Response) -> Response:
        """Set response headers"""
        response.headers['Content-Type'] = 'application/json'
        return response

def register_routes(app: Flask) -> None:
    """Register all API routes"""
    
    # Health check
    @app.route(f'{API_PREFIX}/health', methods=['GET'])
    def health() -> Response:
        """Health check endpoint"""
        return jsonify({
            'status': 'ok',
            'message': 'Server is running',
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        })
    
    # Welcome endpoint
    @app.route('/', methods=['GET'])
    def welcome() -> Response:
        """Welcome message"""
        return jsonify({
            'name': 'MovieZone Integrated Server',
            'version': '1.0.0',
            'description': 'Unified Telegram Bot + Web Server',
            'api_docs': f'{API_PREFIX}/health',
            'admin_panel': '/admin.html'
        })
    
    # Admin panel
    @app.route('/admin.html', methods=['GET'])
    def admin_panel() -> Response:  # type: ignore
        """Serve admin panel"""
        return app.send_static_file('admin.html')
    
    # Placeholder for movie routes
    @app.route(f'{API_PREFIX}/movies', methods=['GET'])
    def get_movies() -> Response:
        """Get all movies (placeholder)"""
        return jsonify({
            'status': 'success',
            'data': [],
            'message': 'Movie routes coming soon'
        })
    
    # Admin login
    @app.route(f'{API_PREFIX}/admin/login', methods=['POST'])
    def admin_login() -> Union[Response, tuple[Response, int]]:
        """Admin login"""
        from config import ADMIN_ID, ADMIN_PASSWORD
        data = request.get_json()
        if data.get('admin_id') == ADMIN_ID and data.get('password') == ADMIN_PASSWORD:
            return jsonify({'status': 'success', 'message': 'Login successful'})
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    
    # Add movie
    @app.route(f'{API_PREFIX}/admin/movies', methods=['POST'])
    def add_movie() -> Union[Response, tuple[Response, int]]:
        """Add new movie"""
        from config import ADMIN_ID, ADMIN_PASSWORD
        data = request.get_json()
        # Simple auth check (in production use proper auth)
        if data.get('admin_id') != ADMIN_ID or data.get('password') != ADMIN_PASSWORD:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        # Add to database
        from database import get_db_session
        from database.models import MovieLink
        import uuid
        
        with get_db_session() as session:
            movie = MovieLink(
                movie_name=data['movie_name'],
                original_link=data['original_link'],
                short_id=str(uuid.uuid4())[:6]
            )
            session.add(movie)
            session.commit()
        
        return jsonify({'status': 'success', 'message': 'Movie added', 'short_id': movie.short_id})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error: Exception) -> Union[Response, tuple[Response, int]]:
        """Handle 404 errors"""
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found',
            'path': request.path
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error: Exception) -> Union[Response, tuple[Response, int]]:
        """Handle 500 errors"""
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
    
    logger.info("✅ Routes registered")
