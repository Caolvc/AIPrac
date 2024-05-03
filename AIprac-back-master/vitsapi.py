import re
# import httpx
import random



class VITSAPI:

    # client = httpx.AsyncClient(timeout=60, headers={
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    # })

    speaker_map = {
        # "芙宁娜": ["芙宁娜_ZH"],

        "幼年男性": ["托克_ZH"],
        "幼年女性": ["克拉拉_ZH"],
        "少年男性": ["空_ZH", "行秋_ZH"],
        "少年女性": ["荧_ZH", "珊瑚宫心海_ZH", "胡桃_ZH"],
        "青年男性": ["迪卢克_ZH", "达达利亚_ZH"],
        "青年女性": ["夜兰_ZH", "八重神子_ZH"],
        "中年男性": ["戴因斯雷布_ZH"],
        "中年女性": ["凝光_ZH"],
        "老年男性": ["天叔_ZH"],
        "老年女性": ["萍姥姥_ZH"],

        "旁白": ["钟离_ZH"],
        "default": ["钟离_ZH"]
    }


    emotion_map = {
        
    }

    random_seed = random.randint(111111, 666666)

    """
    frags = [
        {
            name: str,
            emotion: str,
            text: str
        }
    ]

    """
    def split_label_txt(self, label_txt: str) -> list[dict]:
        labels = re.findall(r'<.+?>', label_txt)
        txts = re.split(r'<.+?>', label_txt)
        ptr_label = 0
        ptr_txt = len(txts) - len(labels)

        frags = []
        while ptr_label < len(labels):
            name, emotion = re.findall(r'<(.+?):(.+?)>', labels[ptr_label])[0]
            frags.append({
                'name': name,
                'emotion': emotion,
                'text': txts[ptr_txt]
            })
            ptr_label += 1
            ptr_txt += 1

        return frags

    def map_speaker_params(self, name: str):
        if name in self.speaker_map:
            id = self.random_seed % len(self.speaker_map[name])
            return self.speaker_map[name][id]
        else:
            id = self.random_seed % len(self.speaker_map["default"])
            return self.speaker_map["default"][id]


    def map_emotion_params(self, emotion: str, frag: dict) -> None:
        # 这里还缺一个情感映射字典
        frag['sdp'] = 0.6
        frag['noise'] = 0.6
        frag['noisew'] = 0.8
        frag['length'] = 1
        frag['emo'] = 0


    def vocal_url(self, speaker: str, text: str, sdp: float=0.4, noise: float=0.6, noisew: float=0.8, length: float=1, emo: int=0, **kargs):
        return f'https://genshinvoice.top/api?text={text}&sdp={sdp}&speaker={speaker}&noise={noise}&noisew={noisew}&length={length}&emotion={emo}&language=ZH&format=wav'
    
    def get_wav_url_list(self, label_txt: str):
        self.random_seed = random.randint(111111, 666666)
        frags = self.split_label_txt(label_txt)
        url_lst = []
        for frag in frags:
            frag['speaker'] = self.map_speaker_params(frag['name'])
            self.map_emotion_params(frag['emotion'], frag)
            url_lst.append(self.vocal_url(**frag))

        return url_lst

    def set_speaker(self, name:str, value: str):
        if value in self.speaker_map:
            self.speaker_map[name] = self.speaker_map[value]
        



# if __name__ == '__main__':
#     vits = VITSAPI()
#     print(vits.get_wav_url_list("""<小依:愤怒> “请不要这样!”<旁白:平静> 小依怒吼着。
# 小依积累的情绪在那一刻爆发了出来，泪水不知不觉间已经倾泻而出。
# <小依:愤怒> “我不需要你假心假意的关心！”
# <小风:慌忙> “小依……不！不是这样的！这是因为……”
# <旁白:平静> 小风被小依的表现惊到了，慌忙解释到。
# <小依:愤怒> “快滚！滚啊！”
# <幼年男性:疑惑> “哥哥姐姐们在吵什么呀……”<旁白:平静> 一位路过的小男孩问道。
# <中年女性:平静> “嘘！这就是爱情的烦恼。”<旁白:平静> 那位男孩的妈妈回答道。"""))
    