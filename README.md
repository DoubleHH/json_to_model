# 脚本简介

> 作者：huanghui  
> 用于将字典解析成对应写好property的.h.m文件内容，并输出到shell

# 使用方法

```
python jsonmodel_decoder.py complex_json.txt BDExample
```
### 详解：

python jsonmodel_decoder.py 代表执行脚本  
complex_json.txt 代表原始数据文件，以服务端字典的方式呈现  
BDExample 代表Model的前缀，会自动补全后缀model。最终编程BDExampleModel

### 注意：
```
1. 输出到文件，执行以下脚本可以输出到1.txt内  
python json_decoder.py goal_data.txt BDExample > 1.txt

2. 默认的Model前缀是短的，如果需要长的前缀可以加上-l参数，即：  
python json_decoder.py goal_data.txt BDExample -l > 1.txt

3. json文件，数组元素的最后一个item及字典的最后元素都不要加逗号，否则会报
   ValueError: Expecting property name: line 5 column 1 (char 102)
   
   例如：
   {
        "is_authed": "1",
        "sp_balance_quota": "100000",
        "sp_card_quota": "2000000",
	}
	最后字段sp_card_quota后面多了一个逗号。
	改成：
	{
        "is_authed": "1",
        "sp_balance_quota": "100000",
        "sp_card_quota": "2000000"
	}
```