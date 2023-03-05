"""
    WebUI extension launch script
"""

import json
from pathlib import Path
import shutil

here=Path(__file__).parent
ext_base=here.parent
here_tags=here / "tags"

tag_file="danbooru.csv"
if any((autocomplete_tags:=f.parent) for f in ext_base.glob(f"*/tags/{tag_file}")): # 安装了 tag-autocomplete
    shutil.copytree(here_tags,autocomplete_tags,dirs_exist_ok=True)

mix_localization=False
if mix_localization:
    here_locs=here / "localizations"
    zh_file="zh_CN.json"
    if any((zh_localization:=f.parent) for f in ext_base.glob(f"*/localizations/{zh_file}")):
        zh_json=zh_localization / zh_file
        with zh_json.open(encoding="utf-8") as f:
            zh_dict:dict[str,str]=json.load(f)
        here_json=here_locs / "localization-zh.json"
        with here_json.open(encoding="utf-8") as f:
            here_dict:dict=json.load(f)
        zh_dict.update(here_dict)
        rename_item={
            "(":"（",
            ")":"）"
        }
        rename_dict={ 
            k:renamed 
            for k,v in zh_dict.items() 
            if (renamed:=v) and any( 
                (renamed:=renamed.replace(i,rename_item[i])) 
                for i in rename_item 
                if i in renamed 
            )
        }
        zh_dict.update(rename_dict)
        mix_json=here_locs / zh_file
        mix_json=mix_json.with_stem(f"{mix_json.stem}_mixed")
        with mix_json.open("w",encoding="utf-8") as f:
            json.dump(zh_dict,f,ensure_ascii=False,indent=4)

