import json
from annimation_list import *

def remove_function_annimation_list():
    tmp_annimation_list = annimation_list;
    for i in range(len(tmp_annimation_list)):
        if "function" in tmp_annimation_list[i]:
            del tmp_annimation_list[i]["function"];
    return tmp_annimation_list;
