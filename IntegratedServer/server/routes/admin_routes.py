# IntegratedServer/server/routes/admin_routes.py
# Admin & Owner routes - ported from Movieweb + new owner/admin management

from flask import request, jsonify
from server.routes import admin_bp
from database.supabase_client import supabase
import os


# Owner credentials (hardcoded)
OWNER_LOGIN_ID = os.getenv('OWNER_LOGIN_ID', 'sbiswas1844')
OWNER_LOGIN_PASSWORD = os.getenv('OWNER_LOGIN_PASSWORD', 'save@184455')


@admin_bp.route('/api/admin-login', methods=['POST'])
def admin_login():
    """Login for owner (/sudip) or admin (/admin)"""
    try:
        data = request.get_json()
        login_id = data.get('adminId', data.get('admin_id', ''))
        password = data.get('adminPassword', data.get('admin_password', ''))

        if not login_id or not password:
            return jsonify({'error': 'ID and password required'}), 400

        # Check owner first (hardcoded)
        if login_id == OWNER_LOGIN_ID and password == OWNER_LOGIN_PASSWORD:
            return jsonify({
                'success': True,
                'role': 'owner',
                'adminId': login_id,
                'message': 'Owner login successful'
            })

        # Check admin accounts table
        rows = supabase.select('admin_accounts', '*', {
            'admin_id': login_id,
            'is_active': True
        })
        if rows and rows[0].get('admin_password') == password:
            return jsonify({
                'success': True,
                'role': 'admin',
                'adminId': login_id,
                'displayName': rows[0].get('display_name', ''),
                'message': 'Admin login successful'
            })

        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/admin-config', methods=['GET'])
def get_admin_config():
    """Get admin config (owner ID for frontend)"""
    return jsonify({
        'adminId': OWNER_LOGIN_ID,
        'hasCredentials': True
    })


@admin_bp.route('/api/admin-accounts', methods=['GET'])
def get_admin_accounts():
    """Get all admin accounts (owner only)"""
    try:
        accounts = supabase.select('admin_accounts', 'id,admin_id,display_name,is_active,created_at')
        return jsonify(accounts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/admin-accounts', methods=['POST'])
def create_admin_account():
    """Create a new admin account (owner only)"""
    try:
        data = request.get_json()
        admin_id = data.get('adminId', data.get('admin_id', ''))
        password = data.get('adminPassword', data.get('admin_password', ''))
        display_name = data.get('displayName', data.get('display_name', ''))

        if not admin_id or not password:
            return jsonify({'error': 'Admin ID and password required'}), 400

        result = supabase.insert('admin_accounts', {
            'admin_id': admin_id,
            'admin_password': password,
            'display_name': display_name,
            'is_active': True,
            'created_by': OWNER_LOGIN_ID
        })

        return jsonify({
            'success': True,
            'message': f'Admin account "{admin_id}" created',
            'account': result
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/admin-accounts/<int:account_id>', methods=['DELETE'])
def delete_admin_account(account_id):
    """Delete an admin account"""
    try:
        supabase.delete('admin_accounts', {'id': account_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/admin-accounts/<int:account_id>/toggle', methods=['PATCH'])
def toggle_admin_account(account_id):
    """Toggle admin account active status"""
    try:
        data = request.get_json()
        is_active = data.get('isActive', data.get('is_active', True))
        supabase.update('admin_accounts', {'is_active': is_active}, {'id': account_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
