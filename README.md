AcUpload
==========
Acfun乐视云上传脚本，方便折腾黑科技的熊孩子们。

对于经常IO错误者有奇效。


Usage
--------
需要Python2。

cookie文件名是./accookies  .

格式：`Hm_lvt_49129538199e82fd3d7af**********=1398******; bdshare_firstime=*****66321693; Hm_lvt_bc75b9260fe72ee**********=139826***; auth_key=******; auth_key_ac_sha1=-*****; ac_username=****; ac_userimg=http%3A%2F%2Fstatic.acfun.com%2Fdotnet%2F20120923%2Fstyle%2Fimage%2Favatar.jpg; ac_member_guide=0%2C0%2*****; clientlanguage=zh_CN`

    python3 acupload.py (-h/--help) (-e/--examine) (-c/--cookie ./cookiepath) 
                        (-t/--proxy-type [h/s]) (-p/--proxy-address 127.0.0.1:8080)
                        (-a/--curl-args -V)
    
    -h/help: Default: None
        Print this usage file.
        
    -e/examine: Default: 0
        If enabled, acupload will examine all the uploads via the API.
        May return 404 if the speed is too fast.
    
    -c/cookie: Default:'./accookies'
        Set the path of cookie.
    
    -t/proxy-type: Default: Blank
        Set the type of proxy, if you want to use.
        s: SOCKS
        h: HTTP
    
    -p/proxy-address: Default: Blank
        Set the proxy address, if enabled by -t.
        Format:
        127.0.0.1:8080
    
    -a/curl-args: Default: Blank
        Other arguments you want ot put on curl.


文件大小是胡写的，理论上可以上传巨大文件。但是具体啥样就不知道了。死了别找我。

License
----

GPL v3.

Misc
----

* 这个branch是自动转换的，简单测试没问题。
* 晚上写的，肚子饿了，有问题谅解，也没做PEP-8，随便看看吧。
* 禁止转载到**墙内**各种电子公告服务（包括但不限于百毒贴吧、AC 丧尸岛、各种论坛、微博等）。发现腿打折。之前不是没有过先例。

历史
----
0.05: 紧急处理uu限制

0.04：加入代理；加入cookie文件设置；几乎重写了所有模块；巨量错误处理；换自己的UA；显示服务器IP；可选检验

0.03：可以上传巨大文件

0.025：换协议，换UTF-8

0.021：紧急换域名

0.02： 重写进度条

0.01：第一个版本
#### `vu` 的用法
* <http://yuntv.letv.com/bcloud.swf?uu=！！！！！！！！&vu=cd09b2f515>
* `[localup]cd09b2f515[/localup]`
* 乐视云视频 - cd09b2f515