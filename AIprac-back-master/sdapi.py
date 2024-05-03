import httpx
BaseUrl = 'http://localhost:7860'

class SDAPI():
  client = httpx.AsyncClient(timeout=60, proxies=None)

  txt2img_default_params = {
    "prompt": "",
    "negative_prompt": "nsfw,(low quality,normal quality,worst quality,jpeg artifacts),cropped,monochrome,lowres,low saturation,((watermark)),(white letters), skin spots,acnes,skin blemishes,age spot,mutated hands,mutated fingers,deformed,bad anatomy,disfigured,poorly drawn face,extra limb,ugly,poorly drawn hands,missing limb,floating limbs,disconnected limbs,out of focus,long neck,long body,extra fingers,fewer fingers,(multi nipples),bad hands,signature,username,bad feet,blurry,bad body",
    "seed": -1,
    "subseed": -1,
    "sampler_name": "DPM++ 3M SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 20,
    "cfg_scale": 10,
    "width": 512,
    "height": 768
  }

  async def text2img(self, prompt, negative_prompt=txt2img_default_params['negative_prompt'], height=768, width=512):
    params = self.txt2img_default_params.copy()
    params['prompt'] = 'masterpiece, best quality, 4k, 8k, highres, ultra-detailed, ' + prompt
    params['negative_prompt'] = negative_prompt
    params['height'] = height
    params['width'] = width
    print(params)
    res = await self.client.post('http://localhost:7860/sdapi/v1/txt2img',
                                 headers={
                                   'accept': 'application/json',
                                   'Content-Type': 'application/json'
                                 },
                                 json=params)
    return res

