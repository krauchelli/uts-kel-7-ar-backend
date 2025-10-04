from flask import jsonify

def register_error_handlers(app):
    """Registers functions to handle specific HTTP error codes."""

    @app.errorhandler(400)
    def bad_request(error):
        """Handler for Bad Request errors (client-side errors)."""
        response = {
            "success": False,
            "error": "Bad Request",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid request format."
        }
        return jsonify(response), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handler for Internal Server Errors (server-side errors)."""
        response = {
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }
        return jsonify(response), 500