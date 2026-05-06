import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "back"))
from main import app
for route in app.routes:
    print(f"{route.path} [{','.join(route.methods)}]")
