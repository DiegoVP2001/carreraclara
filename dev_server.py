"""Local dev server for Carrera Clara.

Serves web/ while applying the same rewrites Vercel uses in production
(see web/vercel.json). A plain `python -m http.server` does NOT apply them,
so "/" would return a directory listing instead of the landing page and the
header brand link would look broken.

    python dev_server.py        # http://localhost:8000

Also sends Cache-Control: no-store so the service worker does not serve
stale HTML while reviewing changes.
"""
import http.server
import json
import socketserver
from pathlib import Path

PORT = 8000
WEB_DIR = Path(__file__).resolve().parent / "web"


def load_rewrites():
    """Read the rewrite table straight from vercel.json so both stay in sync."""
    config = WEB_DIR / "vercel.json"
    if not config.exists():
        return {}
    rules = json.loads(config.read_text(encoding="utf-8")).get("rewrites", [])
    return {r["source"]: r["destination"] for r in rules}


REWRITES = load_rewrites()


class RewriteHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean in REWRITES:
            path = REWRITES[clean]
        return super().translate_path(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Threaded: un solo hilo (TCPServer liso) hace que fetch() concurrentes
    (ej. el service worker cacheando en segundo plano + un click en "Agregar")
    se encolen y uno quede esperando indefinidamente al otro."""

    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    if not WEB_DIR.is_dir():
        raise SystemExit(f"No existe {WEB_DIR} — corre este script desde el repo.")

    with Server(("127.0.0.1", PORT), RewriteHandler) as httpd:
        print(f"Carrera Clara en http://localhost:{PORT}")
        for source in REWRITES:
            print(f"  http://localhost:{PORT}{source}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDetenido.")
