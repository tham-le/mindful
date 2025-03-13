"""
Authentication routes for MindfulWealth application
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from models import User

# Create blueprint
auth_bp = Blueprint('auth', __name__)

def setup_auth_routes(db_session: Session):
    """
    Set up authentication routes with the provided database session
    
    Args:
        db_session (Session): SQLAlchemy database session
    """
    auth_service = AuthService(db_session)
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Register a new user"""
        data = request.json
        
        # Validate input
        if not all(k in data for k in ['name', 'email', 'password']):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Register user
        success, result = auth_service.register_user(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        if not success:
            return jsonify({'success': False, 'message': result}), 400
        
        # Create tokens
        access_token = create_access_token(identity=result.id)
        refresh_token = create_refresh_token(identity=result.id)
        
        return jsonify({
            'success': True,
            'user': result.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Login a user"""
        data = request.json
        
        # Validate input
        if not all(k in data for k in ['email', 'password']):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Authenticate user
        success, result = auth_service.login_user(
            email=data['email'],
            password=data['password']
        )
        
        if not success:
            return jsonify({'success': False, 'message': result}), 401
        
        # Create tokens
        access_token = create_access_token(identity=result.id)
        refresh_token = create_refresh_token(identity=result.id)
        
        return jsonify({
            'success': True,
            'user': result.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    @auth_bp.route('/demo', methods=['POST'])
    def create_demo():
        """Create a demo user"""
        try:
            demo_user = auth_service.create_demo_user()
            
            # Create tokens
            access_token = create_access_token(identity=demo_user.id)
            refresh_token = create_refresh_token(identity=demo_user.id)
            
            return jsonify({
                'success': True,
                'user': demo_user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @auth_bp.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        """Refresh access token"""
        current_user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Create new access token
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200
    
    @auth_bp.route('/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        """Get current user information"""
        current_user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
    
    @auth_bp.route('/preferences', methods=['PUT'])
    @jwt_required()
    def update_preferences():
        """Update user preferences"""
        current_user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.json
        
        # Update user preferences
        if 'theme_preference' in data:
            user.theme_preference = data['theme_preference']
        
        if 'layout_preference' in data:
            user.layout_preference = data['layout_preference']
        
        if 'language_preference' in data:
            user.language_preference = data['language_preference']
        
        if 'personality_preference' in data:
            # Validate personality preference
            if data['personality_preference'] in ['nice', 'funny', 'irony']:
                user.personality_preference = data['personality_preference']
        
        if 'name' in data:
            user.name = data['name']
        
        # Save changes
        try:
            db_session.commit()
            return jsonify({
                'success': True,
                'user': user.to_dict()
            }), 200
        except Exception as e:
            db_session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return auth_bp 