import tkinter as tk
from tkinter import Scrollbar
from bilibiliQRLogin import bilibiliQRLogin
from config import logger
import time,os
from wordListFile import *
from biliLiveTool import *
import ttkbootstrap as ttk
from PIL import Image,ImageTk

class biliLiveBanword():
    def __init__(self):
        self.user = bilibiliQRLogin()
        loginFlag = self.user.check_expire()  
        self.jsonFilePath = ".\\wordlist.json"
        self.wordjson =  get_all_list(self.jsonFilePath)
        self.csrf = ""
        self.root =ttk.Window(themename="litera")
        self.root.title("屏蔽词小程序")
        self.root.geometry("1024x768")


        #添加页签

        ##如果没有登录
        if (not loginFlag):
            # 创建登录按钮
            self.login_button = tk.Button(self.root, text="登录", font=("黑体", 12),width=20, height=3,  borderwidth=3, relief="raised",command=self.login_clicked)
            self.login_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            #login_button.pack(padx=10, pady=10)
            # 创建显示文字的 Label
            self.text_label = tk.Label(self.root, text="您尚未登录，请先登录！", font=("黑体", 12))
            self.text_label.grid(row=0, column=0, padx=10, pady=(100,10), sticky="nw")

            self.text_label2 = tk.Label(self.root, text="点击登录刷新二维码", font=("黑体", 12))
            self.text_label2.grid(row=0, column=0, padx=50, pady=(150,5), sticky="nw")
        
            # 创建左侧的图片框-扫码
            self.image_frame = tk.Frame(self.root, width=300, height=300, bg="lightgrey")
            self.image_frame.grid(row=0, column=0, padx=10, pady=180, sticky="nw")  #180像素开始

            self.qr_code_lable= tk.Label(self.image_frame)
            self.qr_code_lable.pack(padx=10, pady=10)
        else :
            self.csrf = self.user.login_session.cookies._cookies[".bilibili.com"]["/"]["bili_jct"].value
            uname = getUserInfo(self.user.login_session)
            self.text_label = tk.Label(self.root, text="欢迎您，\n"+ uname, font=("黑体", 12))
            self.text_label.grid(row=0, column=0, padx=10, pady=(100,10), sticky="nw")
        ##备选多选框
        self.text_label3 = tk.Label(self.root, text="备选主题", font=("黑体", 12))
        self.text_label3.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
        self.selectedbox1 = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=20, height=15)
        self.selectedbox1.grid(row=0, column=1, padx=10, pady=(50,10), sticky="nw")


        ##已选多选框
        self.text_label4 = tk.Label(self.root, text="已选主题", font=("黑体", 12))
        self.text_label4.grid(row=0, column=1, padx=(270,0), pady=10, sticky="nw")
        self.selectedbox2 = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=20, height=15)
        self.selectedbox2.grid(row=0, column=1,padx=(270,0), pady=(50,10), sticky="nw")


        # 创建选择按钮
        self.select_button = tk.Button(self.root, text="选择→",font=("黑体", 12), command=self.select_clicked)
        self.select_button.grid(row=0, column=1, padx=(180,0), pady=100, sticky="nw")

        # 创建取消选择按钮
        self.cancel_button = tk.Button(self.root, text="←取消选择",font=("黑体", 12), command=self.cancel_clicked)
        self.cancel_button.grid(row=0, column=1, padx=(160,0), pady=150, sticky="nw")

        self.manage_button = tk.Button(self.root, text="本地屏蔽词清单管理", font=("黑体", 12),command=self.manage_clicked)
        self.manage_button.grid(row=0, column=0, padx=(10,0), pady=400, sticky="nw")

        # 创建已选屏蔽词清单
        self.word_label = tk.Label(self.root, text="已选屏蔽词列表", font=("黑体", 12))
        self.word_label.grid(row=0, column=1, padx=10, pady=(340,5), sticky="nw")

        self.word_box1 = tk.Text(self.root, width=58, height=10,state="disabled")
        self.word_box1.grid(row=0, column=1, padx=10, pady=360, sticky="nw")


        self.add_button = tk.Button(self.root, text="添加到直播间",font=("黑体", 12), command=self.add_word_to_live)
        self.add_button.grid(row=0, column=1, padx=180, pady=(570,5), sticky="nw")

        self.remove_button = tk.Button(self.root, text="从直播间移除",font=("黑体", 12), command=self.remove_word_from_live)
        self.remove_button.grid(row=0, column=1, padx=(300,0), pady=(570,5), sticky="nw")

        self.roomid_label = tk.Label(self.root, text="房间号", font=("黑体", 12))
        self.roomid_label.grid(row=0, column=1, padx=10, pady=(550,5), sticky="nw")

        self.entry_roomid_var = tk.StringVar()
        self.entry_roomid = tk.Entry(self.root, textvariable=self.entry_roomid_var)
        self.entry_roomid.grid(row=0, column=1, padx=10, pady=(570,5), sticky="nw")
      
        self._drawOption(self.wordjson ,self.selectedbox1)
        
        ##日志窗口
        

        self.log_label = tk.Label(self.root, text="日志窗口", font=("黑体", 12))
        self.log_label.grid(row=0, column=2, padx=1, pady=10, sticky="nw")
        
        self.log_frame = tk.Frame(self.root)
        self.log_frame.grid(row=0, column=2,padx=1, pady=(50,10), sticky="nw")  # 设置容器填充满父容器

        self.log_box = tk.Text(self.log_frame, height=30, width=40)
        self.log_box.grid(row=0, column=2,padx=1, pady=0, sticky="nw")
        self.log_box.config(state="disabled")  # 设置文本框状态为不可编辑   
        #self.word_box1.config(state="normal")  # 设置文本框状态为可编辑
        #self.word_box1.delete(1.0, tk.END)     # 清空文本框内容
        scrollbar = Scrollbar(self.log_frame, command=self.log_box.yview)
        scrollbar.grid(row=0, column=3, sticky="ns")
        # 将滚动条与Text控件关联
        self.log_box.config(yscrollcommand=scrollbar.set)
        self.root.mainloop()

    def login_clicked(self):
        oauthKey=self.user.qr_scan()
        self.text_label.config(text="请扫码登录")
        ##二维码路径
        file_path = self.user.qr_path
        if file_path:
            ##在图形页面中展示
            image = Image.open(file_path)  # 使用PIL库打开图像文件
            width, height = image.size
            image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)  # 将图像转换为Tkinter可以使用的PhotoImage对象
            self.qr_code_lable.config(image=photo)  # 在图像标签中显示图像
            self.qr_code_lable.image = photo  # 保持对图像的引用，避免被垃圾回收
        self.root.update_idletasks()

           
        ##等待15秒
        for i in range(self.user.times):
            time.sleep(5)
            status,session = self.user.get_qr_scan_status(oauthKey)
            if status==86101:
                logger.info("等待二维码扫描")
                self.text_label.config(text="等待二维码扫描")
            elif status==86038 :
                logger.info("二维码已失效")
                self.text_label.config(text="二维码已失效")
            elif status==86038 :
                logger.info("已扫码未确认")
                self.text_label.config(text="已扫码未确认")
            elif status==0 :
                logger.info("登录成功")
                self.text_label.config(text="登录成功")
                self.user.login_session = session
                ##保存曲奇
                self.user.save_cookie_to_local()
                self.csrf = self.user.login_session.cookies._cookies[".bilibili.com"]["/"]["bili_jct"].value
                self._redraw_login()
                return session
            if i == self.user.times - 1:
                logger.error('未扫码超时')
                raise TimeoutError("登录超时")
        return None
    def select_clicked(self):
        selected_indices = self.selectedbox1.curselection()
        #删除旧值
        selected_option = []
        wordList = []
        for idx in selected_indices[::-1]:
            ##添加进已选框
            self.selectedbox2.insert(tk.END, self.selectedbox1.get(idx))
            #selected_option.append(selectedbox1.get(idx))
            #删除待备框中的选项
            self.selectedbox1.delete(idx)
        ##重新获取已选，并生成结果集
        optionList = self.selectedbox2.get(0, tk.END)
        self._setBoxWordList(self._getWordList())

    def cancel_clicked(self):
        selected_indices = self.selectedbox2.curselection()
        selected_option = []
        for idx in selected_indices[::-1]:
            ##添加进备选框
            self.selectedbox1.insert(tk.END, self.selectedbox2.get(idx))
            #selected_option.append(selectedbox1.get(idx))
            #删除已选框中的选项
            self.selectedbox2.delete(idx)
        ##重新获取已选，并生成结果集
        self._setBoxWordList(self._getWordList())

    ###子窗口
    def manage_clicked(self):
        child_window = tk.Toplevel(self.root)
        child_window.title("本地屏蔽词管理")
        child_window.geometry("400x500")
        child_window.grab_set()  # 将子窗口设置为模态


        ##主题单选框
        topic_label = tk.Label(child_window, text="主题清单", font=("黑体", 12))
        topic_label.grid(row=1, column=0,sticky="nw",padx=10, pady=0)
        topic_select = tk.Listbox(child_window, selectmode=tk.SINGLE, width=20, height=15,exportselection=False)
        topic_select.grid(row=1, column=0,sticky="nw",padx=10, pady=20)
        entry_var = tk.StringVar()
        del_topic_button = tk.Button(child_window, text="删除该主题",font=("黑体", 12),width=20, height=1,borderwidth=3,command=lambda: self.del_topic(topic_select,word_select))
        del_topic_button.grid(row=1, column=0,padx=10,pady=(250,0))
        entry_topic = tk.Entry(child_window, textvariable=entry_var)
        entry_topic.grid(row=1, column=0,sticky="nw",padx=10, pady=(345,0))
        add_topic_button = tk.Button(child_window, text="添加",font=("黑体", 12),width=10, height=1,borderwidth=2, fg="pink",command=lambda: self.add_topic(entry_topic,topic_select))
        add_topic_button.grid(row=1, column=0,padx=10,pady=(370,0))

        self._drawOption(self.wordjson,topic_select)
        entry_topic.bind("<Return>", lambda event: self.add_topic(entry_topic,topic_select))
        ##该主题的屏蔽词清单
        word_label = tk.Label(child_window, text="屏蔽词列表", font=("黑体", 12))
        word_label.grid(row=1, column=1,sticky='nw',padx=10, pady=0)
        word_select= tk.Listbox(child_window, selectmode=tk.MULTIPLE, width=20, height=15)
        word_select.grid(row=1, column=1,sticky="nw",padx=10, pady=20)
        del_word_button = tk.Button(child_window, text="删除该屏蔽词",font=("黑体", 12),width=20, height=1,borderwidth=3, command=lambda: self.del_word(topic_select,word_select) )
        del_word_button.grid(row=1, column=1,padx=10,pady=(250,0))
        entry_var_word = tk.StringVar()
        entry_word = tk.Entry(child_window, textvariable=entry_var_word)
        entry_word.grid(row=1, column=1,sticky="nw",padx=10, pady=(345,0))
        add_word_button = tk.Button(child_window, text="添加",font=("黑体", 12),width=10, height=1,borderwidth=2, command=lambda: self.add_word(entry_word,topic_select,word_select))
        add_word_button.grid(row=1, column=1,padx=10,pady=(370,0))
        ##绑定选择事件
        topic_select.bind("<<ListboxSelect>>", lambda event: self.show_word_select_manage(self.wordjson,topic_select,word_select))
        entry_word.bind("<Return>", lambda event: self.add_word(entry_word,topic_select,word_select))
    
        ##保存按钮
        save_button = tk.Button(child_window, text="保存当前列表到本地",font=("黑体", 12),width=20, height=1,borderwidth=2, fg="pink",command=self.save_word)
        save_button.grid(row=2, column=0,padx=10,pady=(10,0))
    
    def show_word_select_manage(self,datajson,selectid,targetid):
        selected_indices = selectid.curselection()
        ##添加进备选框
        selected_options =  [selectid.get(idx) for idx in selected_indices]
        if selected_indices:
            #有选择时清空数据
            targetid.delete(0, tk.END)
        if (len(selected_options)==1) :
            for banword in  datajson[selected_options[0]]:
                targetid.insert(tk.END, banword)

    ##输入主题添加项
    def add_topic(self,entry_topic,topic_select):
        val = entry_topic.get()
        if (val!="" and not val.isspace()):
            self.wordjson[val]=[]
            self._drawOption(self.wordjson,topic_select)
        entry_topic.delete(0, tk.END)
        self._redraw();##重绘主页面
    
    ##输入屏蔽词添加项
    def add_word(self,entry_word,topic_select,word_select):
        selected_indices = topic_select.curselection()
        ##添加进备选框
        selected_options =  [topic_select.get(idx) for idx in selected_indices]
        if (len(selected_options)==1) :
            val = entry_word.get()
            if (val!="" and not val.isspace()):
                self.wordjson[selected_options[0]].append(val)
        self.show_word_select_manage(self.wordjson,topic_select,word_select)
        entry_word.delete(0, tk.END)
        self._redraw();##重绘主页面
    ##删除主题项
    def del_topic(self,topic_select,word_select):
        selected_indices = topic_select.curselection()
        selected_options =  [topic_select.get(idx) for idx in selected_indices]
        if selected_indices:
            #有选择时删除数据
            for option in  selected_options:
                if option in self.wordjson:
                    del self.wordjson[option]
        ##重新生成
        self._drawOption(self.wordjson,topic_select)
        ##把右侧屏蔽词列表删除
        word_select.delete(0, tk.END)
        self._redraw();##重绘主页面
    ##删除屏蔽词添加项
    def del_word(self,topic_select,word_select):
        selected_indices = topic_select.curselection()
        ##添加进备选框
        selected_options =  [topic_select.get(idx) for idx in selected_indices]
        if (len(selected_options)==1) :
            selected_indices = word_select.curselection()
            wordList =  [word_select.get(idx) for idx in selected_indices]
            for w in wordList: ##遍历删除
                if w in self.wordjson[selected_options[0]]:
                    self.wordjson[selected_options[0]].remove(w)

        ##重新加载框框
        self.show_word_select_manage(self.wordjson,topic_select,word_select)
        self._redraw();##重绘主页面
    
    #重新绘制主页面的三个框框
    def _redraw(self):
        ##备选框重新绘制
        self._drawOption(self.wordjson,self.selectedbox1) 
        ##绘制空
        self._drawOption({},self.selectedbox2) 
        ##清空文本框
        self.word_box1.config(state="normal")  # 设置文本框状态为可编辑
        self.word_box1.delete(1.0, tk.END)     # 清空文本框内容
        self.word_box1.config(state="disabled")  # 设置文本框状态为不可编辑   
    
    #登录后刷新
    def _redraw_login(self):
        if hasattr(self, "login_button"):
            self.login_button.grid_forget()
        if hasattr(self, "text_label2"):
            self.text_label2.grid_forget()
        if hasattr(self, "image_frame"):
            self.image_frame.grid_forget()
        uname = getUserInfo(self.user.login_session)
        self.text_label.config(text="欢迎您，\n"+ uname)

    def _drawOption(self,wordListJson,boxid) :
        options = list(wordListJson.keys()) 
        ##清空列表
        boxid.delete(0, tk.END) 
        for option in options:
            boxid.insert(tk.END, option)

    #获取已选框中选择主题的屏蔽词（去重)
    def _getWordList(self):
        optionList = self.selectedbox2.get(0, tk.END)
        wordList=[]
        for title in optionList:
            wordList=list(set(wordList+self.wordjson[title]))
        return wordList

    def _setBoxWordList(self,wordList):
        self.word_box1.text=""
        counter = 0
        textStr = ""
        for s in wordList:
            textStr = textStr + s +  ";"
            counter = counter + 1
            if (counter == 6):
                #textStr = textStr + "\n" ## 每六换行
                counter = 0

        self.word_box1.config(state="normal")  # 设置文本框状态为可编辑
        self.word_box1.delete(1.0, tk.END)     # 清空文本框内容
        
        self.word_box1.insert(tk.END, textStr)  # 在文本框末尾插入新的文本内容

        self.word_box1.tag_configure("custom_style", font=("黑体", 14), foreground="blue")
        self.word_box1.tag_add("custom_style", "1.0", tk.END)

        self.word_box1.config(state="disabled")  # 设置文本框状态为不可编辑

    def save_word(self):
        save_all_list(self.wordjson,self.jsonFilePath)
  
    def add_word_to_live(self):
        #获取输入的房间号
        roomid = self.entry_roomid.get()
        #获取已选屏蔽词清单
        word_list = self._getWordList()
        for word in word_list:
            logger.info("添加屏蔽词【"+ word+ "】……") 
            self._logger_out("添加屏蔽词【"+ word+ "】……") 
            code,message = add_live_word_req  (roomid,word,self.user.login_session,self.csrf)
            if code == 0:
                logger.info("添加屏蔽词【"+ word +"】成功")
                self._logger_out("添加屏蔽词【"+ word +"】成功")
            else :
                logger.info("添加屏蔽词【"+ word +"】失败，" + message)
                self._logger_out("添加屏蔽词【"+ word +"】失败，" + message)
    def remove_word_from_live(self):    
        #获取输入的房间号
        roomid = self.entry_roomid.get()
        #获取已选屏蔽词清单
        word_list = self._getWordList()
        for word in word_list:
            logger.info("移除屏蔽词【"+ word + "】……") 
            self._logger_out("移除屏蔽词【"+ word + "】……")
            code,message = remove_live_word_req  (roomid,word,self.user.login_session,self.csrf)
            if code == 0:
                logger.info("移除屏蔽词【"+ word +"】成功")
                self._logger_out("移除屏蔽词【"+ word +"】成功")
            else :
                logger.info("移除屏蔽词【"+ word +"】失败，" + message)
                self._logger_out("移除屏蔽词【"+ word +"】失败，" + message)

    def _logger_out(self,message):
        self.log_box.config(state="normal")
        self.log_box.insert("end", message+'\n')
        self.log_box.see("end")  # 滚动到文本框底部
        self.log_box.config(state="disabled")  # 设置文本框状态为不可编辑   
        self.root.update()
if __name__ == "__main__":
    
    l = biliLiveBanword()
   
    