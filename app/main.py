from fastapi import FastAPI 

app=FastAPI(title="personal blog api")

@app.get("/")
def root():
    return {"message":"welcome to personal blog api"}