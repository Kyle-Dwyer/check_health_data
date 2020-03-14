import pandas as pd
import re
from rule import bad_keyword_list, get_rule_dic, global_list


def compare(num1, num2, option):
    if option == ">":
        return num2 >= num1
    elif option == "<":
        return num2 <= num1
    elif option == "<=":
        return num2 <= num1
    elif option == ">=":
        return num2 >= num1


def check_project_data(project, data, gender):
    if project == 329:
        a = 1

    rule_dict = get_rule_dic(gender)
    normal_flag = False
    if project == 535:
        for bad_word in bad_keyword_list:
            if bad_word in data:
                return normal_flag

    if rule_dict.get(project) is None or data in global_list:
        return True

    if rule_dict[project]['type'] == 0:
        s = re.findall(r"[\(]+[\+\-]+[\)]+",data)
        if len(s) > 0:
            data = data.replace(s[0], "")
        if data == rule_dict[project]['standard']:
            return True
    elif rule_dict[project]['type'] == 1:
        if len(str(data).split('-')) == 2 and str(data).split('-')[0] != '':
            data = (float(str(data).split('-')[0]) + float(str(data).split('-')[1])) / 2.0
        if '(' in str(data):
            print("qqq")
            data = re.findall(r'[(](.*?)[)]', str(data))[0]
        if '（' in str(data):
            data = re.findall(r'（.*?）', str(data))[0].replace('（', '').replace('）', '')
        data = str(data).replace('<', '').replace('>', '')
        # 特例
        if rule_dict[project]['standard'][0] == "Ⅰ":
            return (rule_dict[project]['standard'][1]) >= str(data) >= (rule_dict[project]['standard'][0])
        if float(rule_dict[project]['standard'][1]) >= float(data) >= float(rule_dict[project]['standard'][0]):
            normal_flag = True
    elif rule_dict[project]['type'] == 2:
        if len(str(data).split('-')) == 2 and str(data).split('-')[0] != '':
            data = (float(str(data).split('-')[0]) + float(str(data).split('-')[1])) / 2.0
        if '(' in str(data):
            data = re.findall(r'[(](.*?)[)]', str(data))[0]
        if '（' in str(data):
            data = re.findall(r'（.*?）', str(data))[0].replace('（', '').replace('）', '')
        data = str(data).replace('<', '').replace('>', '')
        if compare(float(rule_dict[project]['standard'][1]), float(data), rule_dict[project]["standard"][0]):
            normal_flag = True
    return normal_flag


if __name__ == '__main__':
    df = pd.read_excel('./data/10people.xlsx')
    df = df.fillna(value='None')
    # print(df.head())
    name_code = {}
    for i in df.columns:
        s = re.findall("(\d+)", i)
        if len(s) > 0:
            num = s[-1]
            name_code[num] = i

    for index, row in df.iterrows():
        exception_list = []
        print('人员编号:', row['人员编号'], '体检时间:', row['体检时间'])
        for project in name_code.keys():
            data = str(row[name_code[project]]).replace("，", "")
            gender = 1 if row["性别"] == "男" else 2
            res = check_project_data(int(project), data, gender)
            # print(str(project) + ":" + str(res))
            if not res:
                exception_list.append((project, data))
        print('异常项目count:', len(exception_list), '得分:', 100 - len(exception_list))
        print('异常项目list:', exception_list)
        print('总检结论（比对用）:', row['总检结论（专家建议）'])
        print('\n')
        # print(row['人员编号'], '/', row['体检时间'], '/', 100 - len(exception_list))
