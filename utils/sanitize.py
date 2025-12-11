"""
Input sanitization utilities to prevent injection attacks and XSS vulnerabilities.
"""

import re


def sanitize_input(user_input):
    """
    Sanitize user input by removing potentially dangerous characters.
    Prevents SQL injection and XSS attacks.
    
    Args:
        user_input: Raw user input string
        
    Returns:
        Sanitized string
    """
    if not isinstance(user_input, str):
        return user_input
    
    # Remove common SQL injection and XSS characters
    dangerous_chars = ['<', '>', '{', '}', '&', ';', '|', '`', '"', "'"]
    sanitized = user_input
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def sanitize_email(email):
    """
    Sanitize email input.
    
    Args:
        email: Email address string
        
    Returns:
        Sanitized email
    """
    if not isinstance(email, str):
        return email
    
    # Remove whitespace and convert to lowercase
    email = email.strip().lower()
    
    # Remove any potentially dangerous characters
    email = sanitize_input(email)
    
    return email


def sanitize_name(name):
    """
    Sanitize name input - allows letters, spaces, and hyphens.
    
    Args:
        name: Name string
        
    Returns:
        Sanitized name
    """
    if not isinstance(name, str):
        return name
    
    # Keep only alphanumeric, spaces, and hyphens
    name = re.sub(r'[^a-zA-Z\s\-]', '', name)
    
    return name.strip()


def sanitize_password(password):
    """
    Sanitize password input - remove whitespace at start/end only.
    Don't remove special characters as they're required for password strength.
    
    Args:
        password: Password string
        
    Returns:
        Sanitized password
    """
    if not isinstance(password, str):
        return password
    
    # Only strip whitespace, preserve all characters for password
    return password.strip()
