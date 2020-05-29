"""App entry point."""
from ClinicalRegex import create_app
import os
import sys
import webview
import threading
app = create_app()
app.url_map.strict_slashes = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath("__file__")))
    return os.path.join(base_path, relative_path)

def start_server():
    # app.run(host='127.0.0.1', port=5000, debug=True)
    kwargs = {'host': '127.0.0.1', 'port': '5000'}
    t = threading.Thread(target=app.run, daemon=True, kwargs=kwargs)
    t.start()

    webview.create_window("Clinical Regex",
                          "http://127.0.0.1:5000")


    webview.start(gui='cef')

    sys.exit()


if __name__ == "__main__":
    start_server()


