def developer_mode(request):
    return {'dev_mode': request.session.get('dev_mode', False)}