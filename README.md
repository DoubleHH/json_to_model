# 脚本简介

> 作者：huanghui  
> 用于将字典解析成对应写好property的.h.m文件内容，并输出到shell

# 使用方法

```
python json_decoder.py goal_data.txt BDExample
```
### 详解：

python json_decoder.py 代表执行脚本  
goal_data.txt 代表原始数据文件，以服务端字典的方式呈现  
BDExample 代表Model的前缀，会自动补全后缀model。最终编程BDExampleModel

### 注意：
```
1. 输出到文件，执行以下脚本可以输出到1.txt内  
python json_decoder.py goal_data.txt BDExample > 1.txt

2. 默认的Model前缀是短的，如果需要长的前缀可以加上-l参数，即：  
python json_decoder.py goal_data.txt BDExample -l > 1.txt
```