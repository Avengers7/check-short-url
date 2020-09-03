# 短链接检测器



## 项目介绍

本项目是一个短链提取、识别工具。重要包含两个模块：从文本数据中进行URL的提取、识别URL中的短链。
![](https://image-host-toky.oss-cn-shanghai.aliyuncs.com/20200903095807.png)



## 使用示例

```bash
# ./data/random_data_one.json是测试用的示例数据
$ python main.py -f ./data/random_data_one.json 

{'https://zeek.ir/huhsdfods': 'zeek.ir', 'https://virl.com/jdfiehoifn': 'virl.com'}
```



## 进度

目前完成了URL提取的简单降噪以及本地（离线）的短链识别。还有以下几个方面需要提升：
- 联网环境下的短链识别
- URL提取的效率、短链识别的效率
- 短链识别的判断逻辑
- URL提取的降噪



## 目录结构

- data：存储测试数据、相关的库数据
- common：通用模块
- extract_url：包，提取URL、TLD等方法
- identfy_url：包，对URL中短链识别相关的方法
- utils：包，相关工具类的方法
- xminds：项目脑图
- docs：项目文档
- requirements.txt：项目依赖