"""Route blueprints. Each module exposes one Blueprint registered in app.py.

Routes are thin: they only handle request parsing, calling services, and
shaping the JSON response. Business logic lives in services/.
"""
