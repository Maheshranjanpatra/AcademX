from functools import wraps
from flask import abort, redirect, url_for, flash, session
from flask_login import current_user
from datetime import datetime, timedelta

SESSION_TIMEOUT = 30  #in min


def admin_required(f):
    """Restrict a route to logged-in admins."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return f(*args, **kwargs)
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.admin_login'))
    return decorated


def check_session_timeout(f):
    """Check session timeout for admin routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'last_activity' in session:
            last_active = session['last_activity']
            if isinstance(last_active, str):
                last_active = datetime.fromisoformat(last_active)
            if datetime.utcnow() - last_active > timedelta(minutes=SESSION_TIMEOUT):
                session.clear()
                flash('Your session has expired. Please log in again.', 'error')
                return redirect(url_for('auth.admin_login'))
        session['last_activity'] = datetime.utcnow().isoformat()
        return f(*args, **kwargs)
    return decorated
