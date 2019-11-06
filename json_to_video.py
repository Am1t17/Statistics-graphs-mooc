
def get_type(module_id):
    return module_id.split('@')[1].split('+')[0]

def get_module_name(module_id,JF:dict):
   return JF['blocks'][module_id]["display_name"]

   
#finding the father module_id
def get_father(module_id,JF:dict):
   for key in JF['blocks']:
      if module_id in JF['blocks'][key]['children']:
         return key
   return None

#geting the name of the video if None the fither's name
def get_video_name(module_id,JF:dict):
   if module_id == None:
      return None
   if (len(JF['blocks'][module_id]['display_name']) > 1) and (JF['blocks'][module_id]['display_name'] != "סרטון"):
      return JF['blocks'][module_id]['display_name']
   else:
      return(get_video_name(get_father(module_id,JF),JF))

def get_dict_video_name(JF:dict):
   cource_name = dict();
   # creating the new cource_name using dict
   for key in JF['blocks']:
      if get_type(key) == 'video':
         cource_name[key] = get_video_name(key,JF)
   return cource_name

def get_class_name(module_id,JF:dict):
   temp_class = get_class(module_id)
   return JF['blocks'][temp_class]['display_name']

def get_class(module_id,JF:dict):
   list = [module_id]
   while module_id != None:
      module_id = get_father(module_id,JF)
      list.append(module_id)
   return list[-3]
def get_subclass(module_id,JF:dict):
   list = [module_id]
   while module_id != None:
      module_id = get_father(module_id,JF)
      list.append(module_id)
   return list[-4]

def get_course(module_id,JF:dict):
   list = [module_id]
   while module_id != None:
      module_id = get_father(module_id,JF)
      list.append(module_id)
   return list[-2]

def get_dict(JF:dict):
   module_course = get_course(list(JF['blocks'].keys())[0],JF)
   my_dict = {}
   video_name = get_dict_video_name(JF)
   main_url = "https://campus.gov.il/courses/course-"+str(module_course).split('-')[1].split('@')[0][:-5]+"/courseware/"
   for key in JF['blocks'][module_course]["children"]:
      my_dict[key] = {"display_name": get_module_name(key,JF),"children":{}}

      for child in JF['blocks'][key]["children"]:
         my_dict[key]["children"][child] = {"display_name": get_module_name(child,JF), "videos": {},
                                "url_link": main_url + str(str(key).split("@")[-1]) + "/" + str(str(child).split("@")[-1])}

   for key, value in video_name.items():
      my_dict[get_class(key,JF)]["children"][get_subclass(key,JF)]["videos"][key] = {"video_name": value}
   return  my_dict












