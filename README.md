#自动化接口测试说明
    [运行环境说明]
    python环境：python 2.7 详细版本号 python 2.7.12rc1
    依赖包：xlrd，xlsxwriter
    手动安装时，在命令行环境下进入相关包文件目录下进行安装，运行 
    python setup.py install
    等待安装结束即可。
    在自动化收集，处理单接口，业务接口前，请先执行 
    python initConfig文件，使配置生效。尤其是更改配置后，请一定执行该文件

#流程说明
模块1：单接口可用性测试
![image](https://github.com/enefuture/InterfaceTesting/blob/master/source/images/1.png)
模块2：业务接口可用性测试
![image](https://github.com/enefuture/InterfaceTesting/blob/master/source/images/2.png)
总流程图：
![image](https://github.com/enefuture/InterfaceTesting/blob/master/source/images/3.png)
详细请参照PTT说明操作。
#配置配置文件
【程序的配置文件】
    在conf/config.py文件下，其中涉及四个配置
    [DATA_PATH] 
        字符串，配置数据的存放路径，默认是项目下的data目录
    [FIDDLER_FILTER_PATH]
        字符串，配置fiddler数据自动收集时配置的文件目录
    [PROJECT_ARRAY]
        数组，配置项目已有的项目接口名称
    [PROJECT_DOMIN]
        字典，与PROJECT_ARRAY中的项目名对应，是指某一项目名称下包含的所有的接口域名
    说明：会在data目录下创建项目文件，并在项目文件中创建单接口目录，业务接口目录，内含source和result目录。
    【人工操作步骤】【!重点说明!】
        每次修改config.my文件后，请执行 python initConfig.py 文件，更新配置
【Fiddler过滤域名配置】
    【人工操作步骤】
    在配置FiddlerRules.js文件中需要注意3处需要改动的地方
    （1） 152-153行，其中包括filterUrl、filePath，含义分别如下：
          filterUrl：需要收集的请求域名，与上述PROJECT_DOMIN中的某一项目的请求域名相对应（就是根据配置文件填写此次需要过滤收集的域名）
          filePath : 收集文件的存储位置，配置为，存储的根路径，与配置文件中的
                     FIDDLER_FILTER_PATH相同。
          projectName：项目名称，更换项目时，记得修改此处的项目名。此处是采用按日期中的天来划分项目的数据文件，apk包大概是一天一个测试版本。
           ![image](https://github.com/enefuture/InterfaceTesting/blob/master/source/images/4.png)
    （2） 278行，其中的函数DivideUrl是划分请求的接口存放文件名方法
           ![image](https://github.com/enefuture/InterfaceTesting/blob/master/source/images/5.png)  
    替换FiddlerRules.js文件，在Fiddler自动收集某一项目的请求数据时，需要配置Fiddler的过滤设置，替换位置在 Rules->Customize Rules,打开后替换全部的内容即可。

#Fiddler自动化数据收集
    首先：运行 python initConfig.py 文件，更新配置
    目的：在对一个项目的接口不熟悉，或者不知道的有多少接口的情况下，可以通过配
          置FiddlerRules.js文件来自动收集该项目的的所有接口请求数据。可以通过收集的文件看是否覆盖全接口，同时为后续的测试接口收集测试用例。大部分是正常的请求数据，所以大部分是正确的case用例。
    【人工操作步骤】【执行时需修改源文件名】 因为是按照日期收集的数据，当执行处理文件时。请将
            D:\\FiddlerFilterApi\\Pop_2016-9-5 文件名重命名为 Pop，
            就是只要项目名称，不要收集的日期
    结果：Fiddler回家配置的过滤收集域名下的所有数据根据函数DivideUrl的区分结果
          ，写入相应的txt数据中,其中用 Session end 区分一条数据的完成.

#处理Fiddler收集数据
    在自动化收集完成后，可以通过 python dealFiddlerFilter.py来解析相应的txt文件，生成excel数据，用作测试人员筛选可行的用例case。
    在执行这一步时，务必保证已经经过了Fiddler的数据自动化收集过程。
    【人工操作步骤】：需要修改配置的 FIDDLER_FILTER_PATH 文件目录下的项目名称，因为项目名称是（项目名+日期），这个需要我们去掉日期，只保留项目名称
    执行方法如下 python dealFiddlerFilter.py 
    收集数据的格式如下：
        {
            "Id": int //一条测试记录的唯一标识，手工填，不要重复
            "Data" : 日期
            "ApiName" : string // 一个接口的名称，手工填，不要重复
            "CaseDesc": string //用例描述
            "Method"：POST/GET…… //请求的方式
            "Http": http/https // 协议
            "Host": string // 域名或者ip
            "Port": int //端口号
            "Path" : string //请求路径，为uri
            "Query" : json //url后跟的参数key-value形式
            "Param": json //请求的参数 ，空请填{}
            "PassParam" : json //业务传递参数
            "Code" : int // 自动化收集时返回状态码
            "Md5": 32位 // 自动化时的MD5
            "Response": json // 自动化收集数据时的返回值
            "CheckPoint" :json  //json格式，空请填写{}下方有其格式及数据的说明,
        }

#人工配置测试用例
    再自动化采集到接口请求数据并成功转成excel数据后，需要人工配置一些数据，如上述中的CaseDesc，CheckPoint，Id等信息，最重要的是CheckPoint的配置，目前支持一层深度的json数据的校验，其中CheckPoint支持相关的key值得相等以及数量的检查。如配置成下列json串：
        {
            "error" : 0,
            "data" : '=30',
            "data" : '<30',
            "data" : '>30',
        }
    上述检查点会去检查一个接口返回的json串的error是否为0，data1的数量是否为30，data2的数量是否小于30，data3的数量是否大于30。暂时只支持这些类型的检查。
    在配置各个接口的测试用例后，可以补充并扩展一些其他的此时用例来验证某个功能，或者来覆盖全用例。
    最好能够将各个接口设计统计到一张excel表中，用一张总表来记录你修改和添加的case用例，这是为了防止下次自动采集的时候覆盖你的修改（！！！*注意点*！！！）

#[单接口测试]
    【说明】
        单接口测试不考虑业务，只考虑这个接口在一次请求是否能够正常返回，主要是根据请求是否成功以及在CheckPoint点的检查是否通过
    【运行程序】
        命令行下输入 ：python singleInterface.py 
        等待处理结束，即可去提示的目录下查看测试结果
#运行结果说明
    运行结果会对应生成每条测试记录的请求结果，其中会增加几个字段，如是否成功，请求的状态码，耗时，错误信息，返回数据
        {
            "Id": int //一条测试记录的唯一标识，手工填，不要重复
            "接口名" : string // 一个接口的名称，手工填，不要重复
            "请求方法"：POST/GET…… //请求的方式
            "Url" : string //请求路径，为uri
            "请求参数": json //请求的参数
            "依赖业务参数": json //业务接口传递的参数
            "抓包返回状态码":int 
            "测试返回状态码":int
            "抓包返回MD5" : 32位
            "测试返回MD5" : 32位
            "抓包返回Json数据": json
            "测试返回Json数据"：json
            "检查点" : json //检查点为json格式，下方有其格式及数据的说明
            "错误状态码"：0/1/2/3/4 状态码，下面有详细介绍
            "错误描述"：string
            "请求耗时" : time // 一次请求的耗时
        }
    其中是否成功的4种状态码结束如下:
        error 状态码说明
            ：0  请求成功，返回数据正常
            ：1  请求失败，code 状态码大于200
            ：2  请求成功，返回数据状态,格式与CheckPoint中不一致
                 包括：返回数据的error状态码与CheckPoint中不一致
                 返回数据格式与CheckPoint中不一致，不为空，数量不匹配等，具体看检查点配置
            ：3  返回数据不为Json格式，无法解析
            : 4  参数错误，请检查相应参数

#[多接口测试：业务测试]
#测试说明
    多接口测试是业务逻辑上的接口测试，各个接口在串行执行的过程中涉及来回传递数据的，与此同时看各个接口是否能够正常返回，主要是根据请求是否成功以及在CheckPoint点的检查是否通过，来回传递的参数是否在上一接口的返回数据中
#配置测试数据
    同理。我们只需要整理相应的业务逻辑的接口串行执行case，形成整个项目的业务层的case用例，当某条接口或某个业务逻辑发生改变，就需要改变相应业务的case用例，方便测试人员的改动和测试，节省大量操作app和网页的时间。
    测试数据格式就是在单接口测试中添加了一个PassParam参数:
        "PassParam": json //请求的参数 ，空请填{}
    其填写的格式如下：
        {
            url中的key：{"id"：测试数据id，"keySet":"测试数据id的返回结果中key的读取路径，用->拼接"}
            ……
        }
    如下：
        {
            "tkuc":{"id":0,"keySet":"data->setCookie"}
        }
     说明当前需要的参数tkuc的值需要去测试数据中id=0的返回结果中的result['data']['setCookie']中去读取，然后会带着去请求当前的url。

#[测试报告]
    测试报告会在对应的 data目录下的项目名称下的单接口或者业务接口的目录下，以日期为后缀的html文件。在浏览器中查看相关的测试结果即可。如：/data/Pop/singleInterface/report_2018-01-2.html




