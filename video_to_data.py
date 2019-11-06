import pandas as pd
import json
import json_to_video as json_vid
import math



def get_type(module_id):
    return module_id.split('@')[1].split('+')[0]

def creat_table_data(data_list : list):

    table = {
        "view": []
    }
    i = 0
    if len(data_list) != 0:
        last_time = data_list[-1]
        size = len(data_list)
        for precent in range(0,100,5):
            print(find_closest(data_list,precent*last_time))
            table["view"].append(round(100*(len(data_list[find_closest(data_list,precent*last_time):])/size)))
        return table
    else:
        return None


    # table = {
    #     "time": [],
    #     "sum": []
    # }
    # t = 1
    # i=0
    # if len(data_list) != 0:
    #     while t<data_list[-1]:
    #         while data_list[i] < t:
    #             i = i+1
    #         table["time"].append(t)
    #         table["sum"].append(len(data_list[i:]))
    #         t=t+5
    #     for i  in range(len(table["time"])):
    #         table["time"][i] =  table["time"][i] -1
    #     return table
    # else:
    #     return None

def find_closest(L: list,number):

    N = math.floor(number/100)
    for i in range(len(L)):
        if L[i] >=N:
            return i

def filter_table_videos(table:str,JF:dict):
    data = pd.read_csv(table, usecols=["module_id", "state", "anonymous_user","module_type"],index_col= None)#collecting relevant colomn

    data.dropna(inplace=True)  # drop null values to avoid errors
    data = data.loc[data.module_type == "video"]
    data.drop_duplicates(inplace=True)
    data.reset_index(inplace=True)

    data.drop(["anonymous_user", "module_type","index"], axis=1, inplace=True)#left only nodule_id and state

    data_dict = {}
    for key in JF['blocks']:            #initialize dict with topic (module_id)
        if get_type(str(key)) =="video":
            data_dict[key] = []
    for i in range(len(data["module_id"])):# running over raw data and insert relevant data
        if data.iloc[i,0] in data_dict.keys():
            temp = json.loads(data.iloc[i,1])
            if 'saved_video_position' in temp.keys():
                saved_video_position = temp['saved_video_position']
                if saved_video_position != "00:00:00":
                    data_dict[data.iloc[i,0]].append(int(saved_video_position.split(":")[2])+
                                                           int(saved_video_position.split(":")[1])*60+
                                                          int(saved_video_position.split(":")[0])*3600)
    for value in data_dict.values():#sorting every module video
        value.sort()
    new_dict = json_vid.get_dict(JF)
    for class_module in new_dict.values():#create the final table using fun "creat_table_data:
        for sub_class_module in class_module["children"].values():
            for key,video_module in sub_class_module["videos"].items():
                video_module["video_graph"] = creat_table_data(data_dict[key])

    return new_dict

def to_sec(time):
    list = time.split(":")
    return int(int(list[0][-3:])*3600 + int(list[1])*60 + int(list[2]))











