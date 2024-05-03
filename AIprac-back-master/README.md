# 阅读器后端

## 如何安装使用

1. 安装Python >= 3.11。如你认为有必要，可以顺便创建虚拟环境这里略。

2. 项目目录执行

```sh
pip install -r requirements.txt
```

3. 打开B站秋叶大佬的SD整合包，打开其API功能，不要设置账密，之后启动WebUI，保留控制台就行。

4. 运行后端

```sh
uvicorn main:app --port 8000
```

5. 按前端中的文档要求打开前端，配合使用即可

6. 注意不要随意关闭terminal。
