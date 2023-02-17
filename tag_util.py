"""  工具脚本  """

from pathlib import Path
from typing import Iterable
import re
import csv

dan=Path("./tags/danbooru.csv")
dan_zh=Path("./tags/danbooru-zh.csv")
dan_untrans=Path("./tags/danbooru-untranslated.csv")

SEP=csv.excel.delimiter # 默认分隔符 ','
ChooseSep=False
ChooseVal=True

chinese_ptn=re.compile(r"[\u4e00-\u9fa5]+")
def has_chinese(s:str):
    """  是否包含汉字  """
    return chinese_ptn.search(s)

def key_file(path:Path,sep:str=SEP):
    """  读取 path 中 tag 的生成器  """
    yield from (key for key,*_ in read_csv(path,sep))
    # with path.open(encoding="utf-8") as f:
    #     yield from (key for key,*_ in split_gen(f,sep))

def key_val_file(path:Path,sep:str=SEP):
    """  读取 path 中 tag、翻译 的生成器  """
    yield from ( (key,vals[-1]) for key,*vals in read_csv(path,sep) if vals) # 忽略没有分隔符的
    # with path.open(encoding="utf-8") as f:
    #     yield from ( (key,vals[-1]) for key,*vals in split_gen(f,sep) if vals) # 忽略没有分隔符的行

def read_csv(path:Path,sep:str=SEP):
    with path.open(encoding="utf-8",newline="") as f:
        yield from filter(None,csv.reader(f,delimiter=sep)) # 忽略空行

# def split_gen(f:TextIO,sep:str=SEP):
#     """  f 每行按 sep 切分的生成器  """
#     return (y.split(sep) for line in f if (y:=line.strip())) # 忽略空行

def write_csv(rows:Iterable,path:Path,mode="w"):
    with path.open(mode,encoding="utf-8") as f:
        wf=csv.writer(f,lineterminator="\n")
        wf.writerows(rows)

def to_key(key:str):
    """  过滤 tag  """
    return key.strip().lower().replace(" ","_") # A key => a_key

val_ts=str.maketrans("()/","（）|") # ()/ => （）| 
def to_val(val:str):
    """  过滤 翻译  """
    return val.translate(val_ts) # 高/矮(翻译) => 高|矮（翻译）

def key_val_filtered(path:Path,sep:str=SEP):
    """  读取 path 中 tag、翻译 并过滤的生成器  """
    return ((to_key(key),to_val(val)) for key,val in key_val_file(path,sep))

if ChooseSep:
    def get_sep(path:Path=None):
        """  输入分隔符  """
        return input(f"分隔符（默认为 {repr(SEP)}）：") or SEP
else:
    def get_sep(path:Path=None):
        if not path:
            return SEP
        with path.open(encoding="utf-8") as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            return dialect.delimiter or SEP

def not_same(old:str,new:str):
    return not new in old

if ChooseVal:
    def choose_val(old:str,new:str):
        """  从 old 和 new 中挑一个，或者两个都要，或者自己指定一个  """
        mix=f"{old}|{new}"
        which=input(f"使用 1 {old}  2 {new}  3 {mix}  4 自己指定：\n")
        if not which or which=="1": # 默认执行 1
            return old
        elif which=="3":
            return mix
        elif which!="2":
            if which.startswith("4"):
                which=which.removeprefix("4").strip()
            new=which
            while newer:=input(f"当前：{new}  空白以确认，其他输入以重新指定：\n"):
                new=newer
        return new
else:
    def choose_val(old:str,new:str):
        """  new 覆盖 old  """
        print(f"{old}  =>  {new}")
        return new
