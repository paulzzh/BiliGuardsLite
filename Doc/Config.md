# BiliBiliHelper 配置文件说明

## [Account] 帐户区域

``BILIBILI_USER`` B站帐户名  
``BILIBILI_PASSWORD`` B站密码

## [Token] 令牌区域 (该区域无需填写)
``ACCESS_TOKEN`` 访问令牌  
``REFRESH_TOKEN`` 刷新令牌  
``CSRF`` CSRF  
``UID`` UID  
``COOKIE`` COOKIE  

## [Function] 功能区域
``CAPSULE`` 扭蛋功能,**True**开启**False**关闭  
``COIN2SILVER`` 硬币换银瓜子,**True**开启**False**关闭  
``GIFTSEND`` 自动送出礼物,**True**开启**False**关闭  
``GROUP`` 应援团签到功能,**True**开启**False**关闭  
``SILVER2COIN`` 银瓜子兑换硬币功能,**True**开启**False**关闭  
``SILVERBOX`` 自动领取银瓜子宝箱,**True**开启**False**关闭  
``TASK`` 自动领取每日任务,**True**开启**False**关闭  
``RAFFLE_HANDLER`` 小电视之类抽奖,**True**开启**False**关闭  

## [Coin2Silver] 硬币兑换银瓜子设置区域
``COIN`` 每天需要兑换多少枚硬币为银瓜子(数字)

## [Live] 直播区域
``ROOM_ID`` 房间号,用于心跳包和礼物送出  

## [Raffle_Handler] 小电视之类的抽奖功能设置区域(细分)
``TV`` 是否参与小电视类抽奖,**True**开启**False**关闭  
``GUARD`` 是否参与大航海抽奖,**True**开启**False**关闭  
``STORM`` 是否参与节奏风暴抽奖,**True**开启**False**关闭  

## [Log] 日志设置区域
``LOG_LEVEL`` 日志等级
> debug : 最全,用与调试和排除Bug(如果不进行开发不推荐)
>> info : 除了调试的信息其他的都有(强烈推荐)
>>> warning : 警告,几乎没有什么信息(强烈不推荐)
>>>> error : 错误,同上(强烈不推荐)
>>>>> critical : 严重错误,同上(强烈不推荐)

## [Other] 其他设置区域
``INFO_MESSAGE`` 欢迎信息,**True**开启**False**关闭  
``SENTENCE`` 名句,强烈推荐开启,**True**开启**False**关闭  

## [pcheaders] pc请求头 (该区域无需填写)
``Accept`` 接受类型
``User-Agent`` 用户代理
``Accept-Language`` 接受语言
``accept-encoding`` 接受编码
``cookie`` cookie
