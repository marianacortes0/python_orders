import os, sys, uvicorn

# El backend ya está en la raíz

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
