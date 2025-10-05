from flask import jsonify

def register_error_handlers(app):
    """Mendaftarkan fungsi untuk menangani kode error HTTP spesifik."""

    @app.errorhandler(400)
    def bad_request(error):
        """Handler untuk error 400 Bad Request."""
        response = {
            "statusCode": 400,
            "message": str(error.description) if hasattr(error, 'description') else "Format request tidak valid.",
            "data": None
        }
        return jsonify(response), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handler untuk error 500 Internal Server Error."""
        response = {
            "statusCode": 500,
            "message": "Terjadi kesalahan tak terduga di server.",
            "data": None
        }
        return jsonify(response), 500