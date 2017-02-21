##About teemo 

域名收集及枚举工具

提莫(teemo)是个侦察兵，域名的收集如同渗透和漏洞挖掘的侦察，故命名为提莫（Teemo）！


该工具主要有三大模块：


利用搜索引擎：

- baidu
- google (需要代理，可能被block)
- bing  （使用cn.bing.com）
- yahoo
- yandex （可能被block,替代方案xml.yandex.com）
- dogpile
- exaland (可能被block)
- ask  （需要代理）
- googleCSE (需要API)

利用第三方站点：

- Alex
- Chaxunla (图形验证码)
- netcraft 
- DNSDumpster
- Virustotal
- ThreatCrowd
- CrtSearch
- PassiveDNS
- GooglCT
- ILink
- sitedossier
- threatminer
- Pgpsearch

利用枚举

- subbrute [https://github.com/TheRook/subbrute](https://github.com/TheRook/subbrute)

##基本使用

* 查看帮助:

```python teemo.py -h```

* 枚举指定域名（会使用搜索引擎和第三方站点模块）:

``python teemo.py -d example.com``

* 使用代理地址:

``python teemo.py -d example.com -x "http://127.0.0.1:9999"``

* 启用枚举模式:

``python teemo.py -b -d example.com``

* 将结果保存到指定文件(默认会跟进config.py中的设置保存到以域名命名的文件中):

``python teemo.py -d example.com -o result.txt``

* 收集域名并扫描指定端口 :

``python teemo.py -d example.com -p 80,443``

##参考

参考以下优秀的工具修改而来:
 
- [https://github.com/ring04h/wydomain](https://github.com/ring04h/wydomain) 
- [https://github.com/aboul3la/Sublist3r](https://github.com/aboul3la/Sublist3r)
- [https://github.com/laramies/theHarvester](https://github.com/laramies/theHarvester)

Thanks for their sharing.

##优缺点

为什么要修改，相对以上优秀工具有什么优缺点？

优点：

1. 使用的搜索引擎和第三方站点更全面，经过实际测试，发现收集的域名会更多。
1. 添加了代理的支持，像google，ask等可以通过指定代理地址去访问，个人使用google较多，所以这个对我很重要。
2. 使用搜索引擎的模块，会收集邮箱地址。
3. 支持多线程，速度比初始版本更快。

缺点：

1. 初始版本，bug很多。但后续会持续更新改进。欢迎提bug。


##相关思维导图
![](http://i.imgur.com/FEPVijM.png)