#!/usr/bin/python3
# encoding=utf-8

import re
import json
import requests
from os import path

area_dict = {"云塘校区": "0030000000002501", "金盆岭校区": "0030000000002502"}
building_list = [
    {
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
    }
]


def main():
    global configurations
    read_from_configurations = False
    # 先检查是否已有配置文件
    if path.exists("config.txt"):
        if input("检测到配置文件，是否读取？[Y/n]").strip().upper() != "N":
            config_content = "".join(open("config.txt", "r", encoding="utf-8").readlines()).split(";")
            if len(config_content) != 5:
                configurations = inputData()
            else:
                configurations = config_content
                read_from_configurations = True
        else:
            configurations = inputData()
    else:
        configurations = inputData()
    print(requestData(configurations))
    
    if not read_from_configurations:
        if input("是否需要保存目前查询设置？[Y/n]").strip().upper() != "N":
            config_file = open("config.txt", "w", encoding="utf-8")
            config_content = ";".join(configurations)
            config_file.write(config_content)
            config_file.close()
    input("按 <ENTER> 以退出……")

def inputData():
    # 获取校区
    for index in range(len(area_dict)):
        print(str(index + 1) + ": " + list(area_dict.keys())[index])
    area_index = int(input("请选择校区：")) - 1
    area_name = list(area_dict.keys())[area_index]
    area_id = area_dict[area_name]
    # 根据校区 index 获取楼栋
    for index in range(len(building_list[area_index])):
        print(str(index + 1) + ": " + list(building_list[area_index].keys())[index])
    building_index = int(input("请选择楼栋：")) - 1
    building_name = list(building_list[area_index].keys())[building_index]
    building_id = building_list[area_index][building_name]
    # 输入房间号
    room = input("目前选中：" + area_name + building_name + "，输入房间号（如 A101）以继续：")
    return [area_id, room, area_name, building_id, building_name]

def requestData(configurations: list):
    area_id = configurations[0]
    room = configurations[1]
    area_name = configurations[2]
    building_id = configurations[3]
    building_name = configurations[4]
    # 生成 post form
    query_form = {
        "jsondata": json.dumps({
            "query_elec_roominfo": {
                "aid": area_id,
                "account": "000001",
                "room": {
                    "roomid": room,
                    "room": room
                },
                "floor": {
                    "floorid": "",
                    "floor": ""
                },
                "area": {
                    "area": area_name,
                    "areaname": area_name
                },
                "building": {
                    "buildingid": building_id,
                    "building": building_name
                }
            }
        }),
        "funname": "synjones.onecard.query.elec.roominfo",
        "json": "true"
    }
    session = requests.session()
    req = session.post(url="http://yktwd.csust.edu.cn:8988/web/Common/Tsm.html", data=query_form)
    data = req.json()['query_elec_roominfo']
    req.close()
    # 从 data 里获取电量
    return_code = int(data['retcode'])
    if return_code != 0:
        return "发生错误：" + str(return_code) + "，" + data['errmsg']
    else:
        pattern = re.compile(r'\S+?([0-9]+\.[0-9]+)')
        remaining_amount = pattern.search(data['errmsg'])[1]
        return area_name + building_name + room + "的剩余电量为 " + remaining_amount

if __name__ == '__main__':
    main()
