"""App entry point."""
from ClinicalRegex import create_app

app = create_app()
app.url_map.strict_slashes = False

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)
