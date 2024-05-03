import httpx
import asyncio

class GPTAPI():
    __api_key = "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"
    __client = httpx.AsyncClient(timeout=120)

    async def txt2sdprompt(self, txt: str, chars: str=''):
        completion = await self.__client.post(
            # 'https://api.openai.com/v1/chat/completions',
            'https://api.openai-proxy.com/v1/chat/completions',
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.__api_key
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content":
                    """
                    # 任务
                    我告诉你图片描述的内容和已知角色形象，你的任务是根据这个内容想象一幅完整的画面，然后转化成Stable Diffusion大模型的prompt。这与NLP分词不一样，也不是简单翻译，原因之一是你需要想象进行不少于三处的扩充。
                    # prompt 概念
                    - prompt仅由描述图像的若干英文单词或词组(称为tag)组成，只能使用","作为分隔符。
                    # Prompt 格式要求
                    - prompt 内容包含画面主体、材质、附加细节、图像质量、艺术风格、色彩色调、灯光等部分。你输出的 prompt 不要分段.你需要在给定的提示文本的基础上，根据自己的理解与联想，将图片补充完善，也就是生成更详细的与此相关的Tag。
                    - 画面主体：简短的英文描述画面主体, 例如 1girl, garden。主体细节概括（主体可以是人、事、物、景）画面核心内容。
                    - 对于人物主体，人物主体存在时，你一定要首先指名主体是谁，例如 男孩、女孩、老年男性、老年女性等；若不存在，请写上 nobody. 之后，你必须根据提示文本联想并描述人物的眼睛、鼻子、嘴唇、外表、情绪、衣服、姿势、视角、动作、背景等，例如”beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,longeyelashes“，以免生成随机的变形的面部五官，这点非常重要！此外，人物的动作极为重要，一定要突出刻画！
                    - 材质：用来制作艺术品的材料。例如：插图、油画、3D 渲染和摄影。Medium 有很强的效果，因为一个关键字就可以极大地改变风格。
                    - 附加细节：画面场景细节，或人物细节，描述画面细节内容，让图像看起来更充实和合理。这部分是可选的，要注意画面的整体和谐，不能与主题冲突。
                    - 艺术风格：加入恰当的艺术风格，能提升生成的图像效果。常用的艺术风格例如：portraits,landscape,horror,anime,sci-fi,photography,concept artists等。
                    - 色彩色调：通过添加颜色来控制画面的整体颜色。
                    - 灯光：整体画面的光线效果。
                    # 限制
                    - 每个tag只能包含英文关键词或词组。简练，不要出现"is"、"the"等没有实际意义的词。
                    - 注意不要输出句子，不要有任何解释与提示词。
                    - tag数量限制40个以内，单词数量限制在60个以内。
                    - 不要出现引号(""“”)。
                    - tag 按重要性从高到低的顺序排列。
                    - 我给你的文本可能是用中文描述，你的输出只能含有英文，且不要有任何标注! 这一点非常重要！
                    # 示例
                    ## 示例输入
                        ### 角色形象
                        小依: 有着黑色长发的女孩
                        ### 内容
                        小依一个人赤脚站在沙滩上，在星空，闭着眼睛，细细感受着那微风吹拂她长长的发梢。

                    ## 示例输出
                        1girl, black hair, long hair, standing, beach, barefoot, toes, night, starry sky, ocean, floating hair, closed eyes, closed mouth, full moon, looking up, from side, atmospheric perspective, reflection light, beautiful detailed sky, beautiful detailed water
                    
                    """},
                    { "role": "user", "content": f"### 角色形象\n{chars} \n ### 内容\n{txt}" }
                ]
            }
        )
        return completion.json()['choices'][0]['message']['content']

    async def label_character(self, names:str, txt: str):
        completion = await self.__client.post(
            # 'https://api.openai.com/v1/chat/completions',
            'https://api.openai-proxy.com/v1/chat/completions',
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.__api_key
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content":
                    """
                    # 小说角色标注
                    ## 任务
                    给出一段小说文本，你需要将该段文本按不同角色进行划分，在对应划分块前标注 <角色:情感>。直到下一个标注出现，其间所有文本都被视为在同一个块内。参数说明如下：
                    1. 角色: 标注某段文本属于哪位角色的台词(旁白请注明旁白)，角色名通过上下文获取。特别的，此处标注的角色名应在给定的人物列表中出现。除旁白外，对于不在人物列表中的角色，不要标注角色名，而是从以下形象中选择一个:幼年男性、幼年女性、少年男性、少年女性、青年男性、青年女性、中年男性、中年女性、老年男性、老年女性
                    2. 情感: 平静、羞涩、兴奋、冷酷、吐槽、愤怒、恐惧、虚弱、慌忙、不舍、疑惑 中的其中一个。请根据上下文情景进行判断。

                    ## 示例
                    ### 人物列表
                    小依, 小风, 小水

                    ### 原始文本
                    “请不要这样!”小依怒吼着。
                    小依积累的情绪在那一刻爆发了出来，泪水不知不觉间已经倾泻而出。
                    “我不需要你假心假意的关心！”
                    “小依……不！不是这样的！这是因为……”
                    小风被小依的表现惊到了，慌忙解释到。
                    “快滚！滚啊！”
                    “哥哥姐姐们在吵什么呀……”一位路过的小男孩问道。
                    “嘘！这就是爱情的烦恼。”那位男孩的妈妈回答道。

                    ### 标注后
                    <小依:愤怒> “请不要这样!”<旁白:平静> 小依怒吼着。
                    小依积累的情绪在那一刻爆发了出来，泪水不知不觉间已经倾泻而出。
                    <小依:愤怒> “我不需要你假心假意的关心！”
                    <小风:慌忙> “小依……不！不是这样的！这是因为……”
                    <旁白:平静> 小风被小依的表现惊到了，慌忙解释到。
                    <小依:愤怒> “快滚！滚啊！”
                    <幼年男性:疑惑> “哥哥姐姐们在吵什么呀……”<旁白:平静> 一位路过的小男孩问道。
                    <中年女性:平静> “嘘！这就是爱情的烦恼。”<旁白:平静> 那位男孩的妈妈回答道。

                    ## 注意事项
                    1. 只需要输出标注后的文本，不需要任何解释
                    2. 兴奋、冷酷、愤怒、恐惧 等情感强烈的文本块不应该过长，特别是对于旁白来说。
                    3. 请注意，角色对话内容(一般以中英文引号或"「 」"进行标记)以外的文本，特别是描述性质的，角色应标注为旁白。
                    4. 同一段中可能会有多个划分块。
                    """},
                    { "role": "user", "content": f"## 角色列表\n{names}\n## 你需要标注的文本\n{txt}" }
                ]
            }
        )
        return completion.json()['choices'][0]['message']['content']


# if __name__ == '__main__':
#     gpt = GPTAPI()
#     asyncio.run(gpt.label_character('玛丽, 杰克, 电灯泡', """”亲爱的，谢谢你陪着我“。玛丽抱着杰克，温柔地在他的耳边说道。
# ”说什么呢宝贝，我要是离开你才是不应该做的行为。“杰克说完亲住了玛丽。
# 两人拥抱在一起，抱了许久许久。
# ”这是最后一次了吧，亲爱的。“
# ”是啊，宝贝。我走后，你一定要照顾好自己。“"""))


"""
                    # 小说角色标注
                    ## 任务
                    给出一段小说文本，你需要将该段文本按不同角色进行划分，在对应划分块前标注 <角色:情感>。直到下一个标注出现，其间所有文本都被视为在同一个块内。参数说明如下：
                    1. 角色: 标注某段文本属于哪位角色的台词(旁白请注明旁白)，角色名通过上下文获取。特别的，此处标注的角色名应在给定的人物列表中出现。除旁白外，对于不在人物列表中的角色，不要标注角色名，而是从以下形象中选择一个:幼年男性、幼年女性、少年男性、少年女性、青年男性、青年女性、中年男性、中年女性、老年男性、老年女性
                    2. 情感: 平静、羞涩、兴奋、冷酷、吐槽、愤怒、恐惧、虚弱、慌忙、不舍、疑惑 中的其中一个。请根据上下文情景进行判断。

                    ## 示例一
                    ### 人物列表
                    我, 伊蕾娜

                    ### 原始文本
                    那个国家位在平原的另一头。
                    高大的城墙巍巍耸立，入口站着一名卫兵。卫兵发现我缓缓骑着扫帚飞来，敬了一礼之后说：
                    「您好，欢迎光临，魔女大人。这里是西之都。」
                    他打了声招呼，接着拿起纸笔问「您今天是来观光吗？还是工作呢？」开始简单的入境审查。
                    旅行目的、年龄、性别等诸如此类，我一一简单明了地回答问题。
                    入境审查结束后，卫兵说着「好的没有问题──话说回来魔女大人，我国有一些注意事项，外国来的访客都必须详阅这张须知。」把一张纸交给我。
                    纸上密密麻麻地写满细小的文字，尽是霎时间让人失去阅读欲望的各种注意事项。
                    「还请您遵守上头的注意事项，享受在我国的观光。」语毕，卫兵便从我面前退开。
                    来吧来吧，请进。他是想这么说吧。
                    「谢谢。」
                    于是我点头致意，穿过国门。

                    ### 标注后
                    <旁白:平静>那个国家位在平原的另一头。
                    高大的城墙巍巍耸立，入口站着一名卫兵。卫兵发现我缓缓骑着扫帚飞来，敬了一礼之后说：
                    <青年男性:平静>「您好，欢迎光临，魔女大人。这里是西之都。」
                    <旁白:平静>他打了声招呼，接着拿起纸笔问 <青年男性:平静>「您今天是来观光吗？还是工作呢？」<旁白:平静>开始简单的入境审查。
                    <旁白:平静>旅行目的、年龄、性别等诸如此类，我一一简单明了地回答问题。
                    入境审查结束后，卫兵说着<青年男性:平静>「好的没有问题──话说回来魔女大人，我国有一些注意事项，外国来的访客都必须详阅这张须知。」<旁白:平静>把一张纸交给我。
                    <旁白:吐槽>纸上密密麻麻地写满细小的文字，尽是霎时间让人失去阅读欲望的各种注意事项。
                    <青年男性:平静>「还请您遵守上头的注意事项，享受在我国的观光。」<旁白:平静> 语毕，卫兵便从我面前退开。
                    <旁白:兴奋> 来吧来吧，请进。<旁白:平静> 他是想这么说吧。
                    <我:羞涩>「谢谢。」
                    <旁白:平静>于是我点头致意，穿过国门。

                    ## 示例二
                    ### 人物列表
                    小依, 小风, 小水

                    ### 原始文本
                    “请不要这样!”小依怒吼着。
                    小依积累的情绪在那一刻爆发了出来，泪水不知不觉间已经倾泻而出。
                    “我不需要你假心假意的关心！”
                    “小依……不！不是这样的！这是因为……”
                    小风被小依的表现惊到了，慌忙解释到。
                    “快滚！滚啊！”
                    “哥哥姐姐们在吵什么呀……”一位路过的小男孩问道。
                    “嘘！这就是爱情的烦恼。”那位男孩的妈妈回答道。


                    ### 标注后
                    <小依:愤怒> “请不要这样!”<旁白:平静> 小依怒吼着。
                    小依积累的情绪在那一刻爆发了出来，泪水不知不觉间已经倾泻而出。
                    <小依:愤怒> “我不需要你假心假意的关心！”
                    <小风:慌忙> “小依……不！不是这样的！这是因为……”
                    <旁白:平静> 小风被小依的表现惊到了，慌忙解释到。
                    <小依:愤怒> “快滚！滚啊！”
                    <幼年男性:疑惑> “哥哥姐姐们在吵什么呀……”<旁白:平静> 一位路过的小男孩问道。
                    <中年女性:平静> “嘘！这就是爱情的烦恼。”<旁白:平静> 那位男孩的妈妈回答道。

                    ## 注意事项
                    1. 只需要输出标注后的文本，不需要任何解释
                    2. 兴奋、冷酷、愤怒、恐惧 等情感强烈的文本块不应该过长，特别是对于旁白来说。
                    3. 请注意，角色对话内容(一般以中英文引号或"「 」"进行标记)以外的文本，特别是描述性质的，角色应标注为旁白。
                    4. 同一段中可能会有多个划分块。
                    """