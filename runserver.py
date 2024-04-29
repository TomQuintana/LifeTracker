import uvicorn

print("test")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=3000, reload=True)
