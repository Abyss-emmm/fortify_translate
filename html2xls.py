#encoding:utf-8

from bs4 import BeautifulSoup
import re
import pandas as pd
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("usage %s <html_filename> <xlsx_filename>" % (sys.argv[0]))
        exit()
    html_filename = sys.argv[1]
    xlsx_filename = sys.argv[2]
    soup = BeautifulSoup(open(html_filename,encoding='UTF-8'))
    table_top = soup.find(id="__TOC_12")
    spans = table_top.find_all("span",id=re.compile("^__TOC_12"))
    table_issues = []
    data = [[u'漏洞名称',u'风险值',u'个数',u'Abstract',u'Explanation',u'Recommendation']]
    for span in spans:
        table_issues.append(span.find_next_sibling("table"))
    for t in table_issues:
        data = data+one_issue(t)
    data = translate(data)
    frame = pd.DataFrame(data)
    frame.to_excel(xlsx_filename,index=False,header=False)

def current_dir():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return script_dir

def one_issue(table_issue):
    result = []
    trs = table_issue.find_all("tr",recursive=False)
    info_tr =  trs[0]
    # info is [Abstract, Explanation, Recommendation]
    info = get_info(info_tr)
    detail_tr = trs[3]
    name,risk,risk_num = get_detail(detail_tr)
    tmp = [name,risk,risk_num]+info
    result.append(tmp)
    return result
        
def get_translate_table(path):
    table = {}
    with open (path,"rb") as f:
        for line in f.readlines():
            line = line.decode("utf-8")
            if "=" in line:
                key,value = line.split("=")
                key = key.strip()
                value = value.strip()
                table[key] =  value
    return table

def translate(data):
    dictionary_name = u"漏洞名称翻译.txt"
    dictionary =  os.path.join(current_dir(),dictionary_name)
    print(dictionary)
    name_table = get_translate_table(dictionary)
    risk_table = {'Low':"低",'Medium':"中",'High':"高",'Critical':"危急"}
    for i in range(1,len(data)):
        name = data[i][0]
        risk_level = data[i][1]
        data[i][0] = name_table[name]
        data[i][1] = risk_table[risk_level]
    #    data[i][1],data[i][2] = data[i][2],data[i][1]  #为了方便拷贝做个替换
    return data



def get_info(info_tr):
    result = []
    infotable = info_tr.find("table")
    trs = infotable.find_all("tr",recursive=False)
    #AER is Abstract Explanation Recommendation
    AER_tr = trs[1]
    AER_tables = AER_tr.find_all("table")
    # Abstract_table = AER_tables[0]
    # Explanation_table = AER_tables[1]
    # Recommendation_table = AER_tables[2]
    for t in AER_tables:
        result.append(get_AERdata(t))
    return result

def get_AERdata(AER_table):
    divs = AER_table.find_all("div")
    # print(divs[1].contents)
    # print(divs[1].strings)
    data = "".join(divs[1].strings)
    return data.strip()

def get_detail(detail_tr):
    table = detail_tr.find("table")
    name_tr = table.find("tr",class_="style_101")
    divs = name_tr.find_all("div")
    name_div = divs[0] # divs[1]是风险值
    risk_div = divs[1]
    name = "".join(name_div.strings).strip()
    risk_level = "".join(risk_div.strings).strip()
    src_path_trs = table.find_all("tr",class_="style_105")
    src_paths = []
    for tr in src_path_trs:
        src_path = tr.td.div.string
        index = src_path.find("(")
        src_paths.append(src_path[:index].strip())
    #risk = "%s(%d)" % (risk_level,len(src_paths))
    risk_num = len(src_paths)
    return name,risk_level,risk_num


if __name__ == "__main__":
    main()