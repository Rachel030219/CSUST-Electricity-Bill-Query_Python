# CSUST Electricity Bill Query / 长沙理工大学电费查询: Python ver.

这个小工具被设计用来简化长沙理工大学公寓中心复杂的电费查询流程。相对于从复杂的列表中选择，这个工具将其简化到了几乎只需要输入选项序号及房间号即可操作的程度。

环境需求：

- Python 3
- 键盘

使用指南：下载 [main.py](https://github.com/Rachel030219/CSUST-Electricity-Bill-Query_Python/tree/master/main.py) ，启动。

## 技术细节

该脚本向 `http://yktwd.csust.edu.cn:8988/web/Common/Tsm.html` 发送一个 `POST` 请求，form body 包含：

```json
{
    "jsondata": "jsondata", // String, 由 JSON 格式化得到
    "funname": "synjones.onecard.query.elec.roominfo", // String, 固定内容
    "json": "true" // String, 疑似固定内容
}
```

其中， `"jsondata"` 由如下格式的 JSON 获得：

```json
{
    "query_elec_roominfo": {
        "aid": "0030000000002501", // String, 十六位校区 ID, 左侧为云塘校区，金盆岭为 "…02"
        "account": "000001", // String, 六位校园卡号
        "room": {
            "roomid": "A101", // String, 房间号
            "room": "A101" // String, 同上
        },
        "floor": {
            "floorid": "", // String, 留空不填
            "floor": "" // String, 同上
        },
        "area": {
            "area": "云塘校区", // String, 校区名, 可选 "云塘校区" 或 "金盆岭校区"
            "areaname": "云塘校区" // String, 校区名, 同上
        },
        "building": {
            "buildingid": "450", // String, 楼栋 ID
            "building": "留学生公寓" // String, 楼栋名
        }
    }
}
```

经分析，楼栋名与楼栋 ID 的对应关系如下：

```python
[{
    "16栋A区": "471",
    "16栋B区": "472",
    "17栋": "451",
    "弘毅轩1栋A区": "141",
    "弘毅轩1栋B区": "148",
    "弘毅轩2栋A区1-6楼": "197",
    "弘毅轩2栋B区": "201",
    "弘毅轩2栋C区": "205",
    "弘毅轩2栋D区": "206",
    "弘毅轩3栋A区": "155",
    "弘毅轩3栋B区": "183",
    "弘毅轩4栋A区": "162",
    "弘毅轩4栋B区": "169",
    "留学生公寓": "450",
    "敏行轩1栋A区": "176",
    "敏行轩1栋B区": "184",
    "行健轩1栋A区": "85",
    "行健轩1栋B区": "92",
    "行健轩2栋A区": "99",
    "行健轩2栋B区": "106",
    "行健轩3栋A区": "113",
    "行健轩3栋B区": "120",
    "行健轩4栋A区": "127",
    "行健轩4栋B区": "134",
    "行健轩5栋A区": "57",
    "行健轩5栋B区": "64",
    "行健轩6栋A区": "71",
    "行健轩6栋B区": "78",
    "至诚轩1栋A区": "1",
    "至诚轩1栋B区": "8",
    "至诚轩2栋A区": "15",
    "至诚轩2栋B区": "22",
    "至诚轩3栋A区": "29",
    "至诚轩3栋B区": "36",
    "至诚轩4栋A区": "43",
    "至诚轩4栋B区": "50"
},
{
    "西苑1栋": "1",
    "西苑2栋": "9",
    "西苑3栋": "17",
    "西苑4栋": "25",
    "西苑5栋": "33",
    "西苑6栋": "41",
    "西苑7栋": "49",
    "西苑8栋": "57",
    "西苑9栋": "65",
    "西苑10栋": "74",
    "西苑11栋": "75",
    "东苑4栋": "171",
    "东苑5栋": "130",
    "东苑6栋": "131",
    "东苑9栋": "162",
    "东苑14栋": "132",
    "东苑15栋": "133",
    "南苑3栋": "94",
    "南苑4栋": "95",
    "南苑5栋": "96",
    "南苑7栋": "97",
    "南苑8栋": "98"
}]
```

## LICENSE / 许可证

[反 996 许可证](./LICENSE)