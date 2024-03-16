# python about finance
> 本仓库主要用于分享在量化投资领域的学习经验
> + 相关视频讲解可以关注哔哩哔哩账户“金融Pudding”
> + > + > <img src="https://github.com/FinancePudding/Python_About_Finance/blob/main/assets/bilibil.jpg" width="270" height="353">   
> + 分享的内容不仅仅包含书本上的东西，同时还包含本人在量化投资领域的学习经验，以及相关资源的拓展。
> + 随时欢迎各位留言交流，大家共同学习进步！
# 常用的量化投资学习资源
## 1.人工智能工具
### 1.1 chatGPT 
> openai公司开发，相较于其他人工智能工具，反应速度最快，同时用户体验也是最好的，推荐大家优先使用。
> + 网址：[https://chat.openai.com/](https://chat.openai.com/)
>+ 注册时需要使用Google邮箱或者微软邮箱进行注册才能正常注册成功
>+ 如果之前注册过没有识别成功或者使用中国地区的相关邮箱进行注册会被记录
>+ 需要删除掉浏览器中的cookie才能成功注册使用
### 1.2 通义千问
> 阿里云开发的国产大模型，在GitHub上有开源的相关模型，由于数据库基于中国的资料较多，所以在回答有关中国的问题上具有独特的优势。
> + 聊天网址：[https://tongyi.aliyun.com/](https://tongyi.aliyun.com/)
> + 注册简单，只需要简单使用手机号，获取验证码就可以。
> + 网页在进行分页使用的时候不能自动调整大小，同时使用流式输出的时候速度较慢，不能停留在之前输出的地方查看。需要一直等到模型全部回答完毕才能查看，这是web端需要改进的地方。
### 1.3 文心一言
>百度公司开发的大语言模型，可以直接注册使用
> + 网址：[https://yiyan.baidu.com/](https://yiyan.baidu.com/)
>+ 可以借助文件助手上传文本进行分析，可以添加一些个人数据
### 1.4 AiPPT
>可以根据大纲生成相应PPT的人工智能工具
> + 网址：[https://www.aippt.cn/workspace](https://www.aippt.cn/workspace)
> + 平时没有用过，暂不做评价
### 1.5 Kimi chat
> 可以进行长文本分析
> + 网址：[https://kimi.moonshot.cn/](https://kimi.moonshot.cn/)
> + 平时主要用来写研究生作业
> + 需要看的资料过多的时候可以直接丢给模型进行提问，节省时间和效率。
> + 比文心一言和通义千问相比，能够上传的资料相对较多。
### 1.6 Pika 
> 可以根据描述内容生成相应的视频，或者生成动图
> + 网址：[https://pika.art/](https://pika.art/)
> + 没怎么测试过，暂不评价。
### 1.7 百川大模型
> 国产大模型
> + 网址：[https://www.baichuan-ai.com/home](https://www.baichuan-ai.com/home)
> + 同学推荐的，暂时没用过。
### 1.8 通义千问开源大模型
> 阿里云开源的大语言模型
> + 开源模型网址：[https://github.com/QwenLM/Qwen](https://github.com/QwenLM/Qwen)
> + 开源的大模型比较适合小公司基于个人数据进行微调，形成自己的大模型，以降低企业成本。
> + 开源的相关文档比较全面清晰，环境配置简单。

## 2.人工智能云计算平台
> * [**Vastai**](https://vast.ai/)
> * [**Huggingface**](https://huggingface.co/pricing#endpoints)
> * [**Google Colaborator**](https://colab.research.google.com)
> * [**阿里云**](https://www.aliyun.com/)
> * [**百度智能云**](https://cloud.baidu.com/product-price/bml.html)
> * [**腾讯云**](https://cloud.tencent.com/document/product/851/74108)
> * [**阿里旗下modelscope社区**](https://www.modelscope.cn/datasets)
## 3.人工智能API接口和文档
> * [**openai**](https://platform.openai.com/docs/introduction)
> * [**Azure**](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
> * [**阿里云灵积**](https://help.aliyun.com/zh/dashscope/developer-reference/)

## 4.数据获取网站
> 推荐一些在量化投资过程中方便获取证券市场的数据网站
### 4.1 Tushare数据社区
> 使用十分的方便，但是需要有一定的积分才能具有相应的数据权限。
> + 网址：[https://tushare.pro/](https://tushare.pro/)
> + 有Python的API接口，连接十分方便，注册成功并完善信息可以获得120积分，通过推荐新人注册可以获取相应的积分，但是最高只能刷到660积分
> + 淘宝上有出售相应端口的使用字符串的，100元一年5000积分，数据调取方便，推荐使用。
> + 使用教程可以在本人的哔哩哔哩上查看
### 4.2 CSMAR数据库
> 需要购买才能获取相关数据权限
> + 网址：[https://data.csmar.com/](https://data.csmar.com/)
> + 如果学校已经购买可以通过学校的教育邮箱进行注册，获取同样的数据权限。
> + 有Python的API接口，可以直接安装调用，具体安装连接教程见本人哔哩哔哩视频号。
### 4.3 Wind金融终端
> 学校购买，只能在固定机位使用和调取数据
### 4.4 choice金融终端
> 可以通过学生认证，免费查看一些行业研报和股票数据。
> 部分申万行业指数能够查看，同时具有一些宏观和行业数据可以调取使用。
### 4.5 CEIC数据库
> 学校购买的宏观数据库，获取一些国际数据和中国宏观数据相对比较方便。
> 可以通过学校的VPN离校访问登录
## 5.国际证券市场信息获取网站
### 5.1 Yahoo Finance
> 网址：[https://github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)
### 5.2 Google Finance
> 网址：[https://www.google.com/finance/?hl=zh](https://www.google.com/finance/?hl=zh)
### 5.3 Investing
> 输入中文也可以搜索到对应的国际市场相关股票  
> 网址：[https://cn.investing.com/](https://cn.investing.com/)
## 6.爬虫相关资源
### 6.1 《python3 网络爬虫开发实战》
> 网址——Github仓库：[https://github.com/Python3WebSpider/Python3WebSpider](https://github.com/Python3WebSpider/Python3WebSpider)  
> 简介：爬虫介绍的内容十分的全面，很适合新手入门。  
### 6.2 网课
> **平台**：哔哩哔哩  
> **网课名**：尚硅谷python爬虫教程小白零基础速通  
> **简介**：讲课老师很幽默，讲解的案例很详细，可以配合上面的书一起使用。
### 6.3 代理网站
> **免费代理网站**
> * **89免费代理**：[https://www.89ip.cn/index.html](https://www.89ip.cn/index.html)
> * **云代理**：[http://www.ip3366.net/free/](http://www.ip3366.net/free/)
> * **小幻HTTP代理**：[https://ip.ihuan.me/](https://ip.ihuan.me/)
> * **快代理**：[https://www.kuaidaili.com/free/](https://www.kuaidaili.com/free/)
