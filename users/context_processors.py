"""Context processors for the users app.

Contains processors that add variables to the template context.
"""

def developer_mode(request):
    """Add developer mode status to template context.
    
    Args:
        request: The HTTP request object
        
    Returns:
        dict: Contains dev_mode boolean from session
    """
    return {'dev_mode': request.session.get('dev_mode', False)}