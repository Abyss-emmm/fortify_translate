#encoding:utf-8
import sys
import os


def current_dir():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return script_dir

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
def translate_level(line):
    table = {'L':"低",'M':"中",'H':"高",'C':"危急"}
    tmp = line.split(",")
    tmp[1] = table[tmp[1].strip().upper()]
    return ",".join(tmp)

def translate(src,dst,table):
    with open(src,"rb") as fsrc:
        with open(dst,"wb") as fdst:
            for line in fsrc.readlines():
                line = line.decode("utf-8")
                key = line.split(",")[0].strip()
                if key in table.keys():
                    line = line.replace(key,table[key])
                line = translate_level(line)
                line = line.encode("gbk")
                fdst.write(line)
    print("end")

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    dictionary_name = u"漏洞名称翻译.txt"
    dictionary =  os.path.join(current_dir(),dictionary_name)
    table = get_translate_table(dictionary)
    translate(src,dst,table)
