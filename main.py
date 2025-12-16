from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.ask import askRequest, askResponse
from utils.threadupdate import threadUpdate
from llama_cpp import Llama
import sqlite3

conn = sqlite3.connect('userinfo.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS userinfo (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT,
            name TEXT,
            age INTEGER,
            disease TEXT)
'''); conn.commit()

APP = FastAPI()
APP.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)
LLM = Llama(
    model_path="./models/capstone-q4-k-m.gguf", 
    n_ctx = 4096, 
    n_gpu_layers= 24,
    verbose = True
)
@APP.get("/")
def health():
    return {"status":"ok"}

@APP.post("/ai/ask", response_model=askResponse)
async def ask(req: askRequest):
    pipeline = LLM(
        req.text, max_tokens = 512, temperature= 0.5, top_p = 0.9
        ); answer = pipeline['choices'][0]['text'].strip()
    return askResponse(text = answer)

@APP.get("/ai/info")
def getinfo(userid: int, species: str, name: str, age: int, disease: str):
    conn = threadUpdate()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO userinfo (userid, species, name, age, disease) VALUES (?, ?, ?, ?, ?)''', (userid, species, name, age, disease)); conn.commit(); conn.close()

    return {'user': userid, 'species': species, 'name': name, 'age': age, 'disease': disease}

@APP.get('/ai/findname')
def findbydogname(name: str):
    conn = threadUpdate()
    cursor = conn.cursor()

    cursor.execute('SELECT userid, species, name, age, disease FROM userinfo WHERE name = ?', (name,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {'status': 'Not Found'}
    
    return {
        "userid": row[0], 
        'species': row[1],
        'name': row[2],
        'age': row[3],
        'disease': row[4]
    }