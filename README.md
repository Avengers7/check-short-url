# 短链接检测器

## 目录结构

- data：存储测试数据、相关的库数据
- extract_url：包，提取URL、TLD等方法
- identfy_url：包，对URL中短链识别相关的方法
- utils：包，相关工具类的方法
- xminds：项目脑图
- docs：项目文档
- requirements.txt：项目依赖


## 短网址作用
当我们打开短网址时，其会通过重定向的方式如 302 跳转到一个页面网址

## 短网址形式
短网址通常结构如下：域名/短网址id。
短网址 id 其通常由 26 个大写字母 + 26 小写字母 +10 个数字 即 62 种字符组成，随机生成 6 到 7 个，然后组成对应一个 短网址 id，并存入相应的数据存储服务中。
当短网址被访问的时候，短网址的解析服务，会根据 id 查询到对应页面从而实现相应的跳转。

## 实例
短链接形成
短网址：http://suo.im/5TUxCn
原网址：https://paper.seebug.org/1292/#subdomainbrute

## 现在的思路

- 提取URL（正则或用iocextract）
- 对域名（名字 + 后缀）进行分析
    - 提取TLD（tldextract）
    - 判断长度
    - 检查域名后缀
    - 对比常见短链域名库
- 对域名路径进行分析
    - 是否无明显文本特征
- 请求短链获取响应信息
    - 响应码是否为302

## 扩展
- 是否为恶意链接
    - 调用安全短网址联盟api
- 短链接服务
    - 新浪短网址服务：sina.lt/
    - 百度短网址服务：http://dwz.cn/
    - 腾讯短网址：w.url.cn/
    - 站长工具：suo.im/
    - ft12.com：r6a.cn/ r6d.cn/ r6e.cn/ r6m.cn/ t.cn/
- 短链接生成
    - 调用以上服务的api

## 参考资料
https://cloud.tencent.com/developer/article/1015682