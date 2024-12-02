from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment or use 5001 as default
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 