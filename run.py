# run.py
from app import create_app

# ✅ Cette ligne est cruciale : Gunicorn cherche 'app'
app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
