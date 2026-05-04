import os, sys, uvicorn

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "back"))
os.chdir(os.path.join(os.path.dirname(__file__), "back"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
