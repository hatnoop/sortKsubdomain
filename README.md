## 工具说明：

将ksubdomain工具验证模式扫描结果转换成json格式，并加入cdn识别结果，支持jq命令调用

cdn识别功能借鉴Shuize

## 使用方法：

ksubdomain命令

```
./ksubdomain v -d www.baidu.com --silent -o test.txt
```

将test.txt放到项目路径，使用如下命令

```
python3 main.py -f test.txt -o result.txt

cat result.txt | jq
```

取某一个字段的值

```
cat result.txt | jq '.[]|.subdomain'
```

额外参数（非必要）

```
-d: 保存ip不为空或者ip不为0.0.0.0的子域名
-i: 去重保存所有不为cdn和非内网的ip
```

