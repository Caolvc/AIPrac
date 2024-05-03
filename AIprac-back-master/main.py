from fastapi import FastAPI, Body, Form
from gptapi import GPTAPI
from sdapi import SDAPI
from dbserver import DbServer
from pydantic import BaseModel
from vitsapi import VITSAPI
import json


app = FastAPI()

sd = SDAPI()
gpt = GPTAPI()
db = DbServer()
vits = VITSAPI()

class Txt2imgRequest(BaseModel):
    txt: str


@app.post('/api/sd/txt2img')
async def txt2img_api(req: Txt2imgRequest):
    chars = db.query_characters()
    chars_ap = ''
    for char in chars:
        chars_ap += char['name']
        chars_ap += ': '
        chars_ap += char['desc']
        chars_ap += '\n'
        
    prompt = await gpt.txt2sdprompt(req.txt, chars_ap)
    print(prompt)
    res = await sd.text2img(prompt)
    return res.json()['images'][0]


@app.get('/api/data/novel-list')
async def get_novel_list():
    return db.query_novel_list()


@app.get('/api/data/novel-detail')
async def get_novel_detail(nid: int):
    return db.query_single_novel(nid)


@app.get('/api/data/chapter-list')
async def get_chapter_list(nid: int):
    return db.query_chapter_list(nid)


@app.get('/api/data/chapter-detail')
async def get_chapter_detail(nid: int, cid: int):
    return db.query_single_chapter(nid, cid)


@app.post('/api/vits/txt2wav')
async def get_wav_list(txt=Body()):
    chars = db.query_characters()
    names = ''
    for char in chars:
        names += char['name']
        names += ','
        vits.set_speaker(char['name'], char['voice'])

    label_txt = await gpt.label_character(names, txt)
    print(label_txt)
    return vits.get_wav_url_list(label_txt)


@app.get('/api/data/characters')
async def get_all_characters():
    return db.query_characters()


@app.post('/api/data/new-charater')
async def new_character(name: str = Form(), voice: str = Form(), desc: str|None = Form(None), img: str|None= Form(None)):
    
    return db.new_character(name, voice, desc, img)

@app.post('/api/data/del-character')
async def del_character(chid: int = Body()):
    db.delete_character(chid)
    
