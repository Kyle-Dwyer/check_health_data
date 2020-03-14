import xlrd
import re

global_list = [
    'None',
    '--',
    '---',
    '正常',
    '未见明显异常',
    '未见异常',
    '主诉无',
    '无异常',
    '拒检',
    '婉拒',
    '正常心电图'
]
#
# list1 = ['阴性']
# list2 = ['无']
# list3 = ['(-)']
#
# word_rule_dict = {
#     0: global_list,
#     1: global_list + list1,
#     2: global_list + list2,
#     3: global_list + list3
# }

bad_keyword_list = ['脂肪肝',
                    '钙化',
                    '胆囊壁结晶',
                    '甲状腺结节',
                    '囊肿',
                    '肝脂肪浸润',
                    '点状结晶',
                    '多发结节',
                    '双乳小叶增生',
                    '肌瘤',
                    '肾结晶',
                    '血管瘤',
                    '弥漫性病变',
                    '回声不均匀',
                    '回声欠均匀',
                    '双乳退化不全']

rule_dict_male = {}
rule_dict_female = {}

x1 = xlrd.open_workbook("./data/standards.xls")
sheet1 = x1.sheet_by_name("阈值20200112")

a = 0
b = 0
for i in range(sheet1.nrows - 1):
    gender = 0
    class_code = sheet1.cell_value(i + 1, 0)
    class_name = sheet1.cell_value(i + 1, 1)
    code = sheet1.cell_value(i + 1, 2)
    name = sheet1.cell_value(i + 1, 3)
    judge = str(sheet1.cell_value(i + 1, 4))
    standard = str(sheet1.cell_value(i + 1, 5))
    note = sheet1.cell_value(i + 1, 6)
    # 没有标准的项目
    if note != '' or standard == "NULL" or standard == '' or standard == "本体检中心无此检验项目" or standard == "不做" or "---" in standard or "～" in standard:
        continue

    # 不检查项目
    if class_code == 688 and not (code == 1174 or code == 1171 or code == 547):
        continue
    if class_code == 1444 and code > 1555 and code < 1559:
        continue

    # debug1
    j = "-" in standard or "<" in standard or ">" in standard or "=" in standard
    if j:
        a += 1

    # if (j and s is None) or (not j and s is not None):
    #     print(i + 2)
    #     print(s is not None)
    #     print(standard + "\n")
    if "男" in judge and "女" in judge:
        gender = 3
    elif "男" in judge:
        gender = 1
    elif "女" in judge:
        gender = 2

    if gender != 3:
        type = 0
        boundary = standard.replace("，", "")
        if gender == 1 or gender == 2:
            standard = re.subn("[男女性：]", "", standard)[0]

        s = re.search("(\d+\.{0,1}\d*)*[\D^\.]*(\d+\.{0,1}\d*)", standard)
        # 两个特例
        if standard == "0.0":
            s = None
            type = 1
            boundary = (0, 0)
        if standard == "Ⅰ-Ⅱ":
            b += 1
            type = 1
            boundary = ("Ⅰ", "Ⅱ")

        if s != None:
            b += 1
            type = 1
            boundary = s.groups()
            # print(range)
            # print(standard + "\n")

        if boundary[0] is None:
            type = 2
            num = boundary[1]
            s = standard.replace(" ", "").split(str(num))[0]
            boundary = (s, num)
        tmp_dict = {'type': type, 'standard': boundary}
        if gender == 1:
            rule_dict_male[code] = tmp_dict
        elif gender == 2:
            rule_dict_female[code] = tmp_dict
        else:
            rule_dict_male[code] = tmp_dict
            rule_dict_female[code] = tmp_dict
    else:
        b += 1
        # print(standard)
        s = re.findall(r"\d+\.?\d*", standard)
        if len(s) == 2:
            tmp_dict1 = {'type': 2, 'standard': ("<", s[0])}
            tmp_dict2 = {'type': 2, 'standard': ("<", s[1])}
        else:
            tmp_dict1 = {'type': 1, 'standard': (s[0], s[1])}
            tmp_dict2   = {'type': 1, 'standard': (s[2], s[3])}
            rule_dict_male[code] = tmp_dict1
            rule_dict_female[code] = tmp_dict2

# print("a:" + str(a))
# print("b:" + str(b))
def get_rule_dic(gender):
    return rule_dict_male if gender == 1 else rule_dict_female;
