class MediaContentDispositionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/media/'):
            print(f'Middleware called for: {request.path}')

            # Set Content-Disposition for inline viewing
            response['Content-Disposition'] = 'inline'

            # Set or modify Content-Type
            import mimetypes
            mime_type, _ = mimetypes.guess_type(request.path)
            if mime_type:
                response['Content-Type'] = mime_type

            # Remove or adjust security headers if necessary
            response.headers['X-Frame-Options'] = 'ALLOWALL'  # Allow embedding in iframe
            if 'Cross-Origin-Opener-Policy' in response.headers:
                del response.headers['Cross-Origin-Opener-Policy']

        return response
