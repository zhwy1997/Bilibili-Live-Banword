import json

# {"title1":["keyword1","keyword2"],
#  "title2":["keyword1","keyword2"]
#  }

##新增/修改/删除某一字典项下屏蔽词，批量更新该字典项目
## listName : 字典项
## keywordList: 该项目下清单
## fileName : json文件名
def save_List(listName,keywordList,fileName):
    allWordList={}
    with open(fileName, 'r',encoding="utf-8") as file_object:  ###获取现存所有屏蔽词列表
        line = file_object.read()
        if(line!=''):
            allWordList = json.loads(line)
        ##重新写
    with open(fileName, 'w+',encoding="utf-8") as file_object: 
        allWordList[listName] = keywordList
        json.dump(allWordList,file_object,ensure_ascii=False)


#获取屏蔽词列表清单
#fileName：json文件名
#return 屏蔽词清单,json格式
def get_all_list(fileName):
    allWordList={}
    with open(fileName, 'r',encoding="utf-8") as file_object:  ###获取现存所有屏蔽词列表
        line = file_object.read()
        if(line!=''):
            allWordList = json.loads(line)
    return allWordList



#删除某一字典项
#fileName：json文件名
#listName:字典名
#return 屏蔽词清单,json格式
def del_list(listName,fileName):
    allWordList={}
    with open(fileName, 'r',encoding="utf-8") as file_object:  ###获取现存所有视频资讯的详细讯息
        line = file_object.read()
        if(line!=''):
            allWordList = json.loads(line)
    with open(fileName, 'w+',encoding="utf-8") as file_object: 
        if listName in allWordList:
            del allWordList[listName]
            ##重新写
            content =json.dump(allWordList,file_object,ensure_ascii=False)

        
def save_all_list(keywordJson,fileName):
    ##覆盖写
    with open(fileName, 'w+',encoding="utf-8") as file_object: 
        json.dump(keywordJson,file_object,ensure_ascii=False)