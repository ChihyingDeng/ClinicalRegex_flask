"""App entry point."""
from ClinicalRegex import create_app

app = create_app()
app.url_map.strict_slashes = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
