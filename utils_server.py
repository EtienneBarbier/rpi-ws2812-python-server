import json
from annimation_rainbow_list import *
import copy

def remove_function_annimation_list():
    tmp_annimation_list = copy.deepcopy(annimation_list);
    for i in range(len(tmp_annimation_list)):
        if "function" in tmp_annimation_list[i]:
            del tmp_annimation_list[i]["function"];
    return tmp_annimation_list;
