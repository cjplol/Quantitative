import ollama
import json
import os

#工作目录路径
workspace_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
history_path=os.path.join(workspace_path,"history") #历史对话记录文件目录

#OLLAMA类，参数：模型名
class OLLAMA:
    def __init__(self,modelname='deepseek-r1:32b'):
        self.modelname=modelname
        self.history = []       #对话内容
        self.get_savefile()    #读取现有的历史对话文件

    #获取现有的历史对话文件
    def get_savefile(self):
        self.save_filenames=[f for f in os.listdir(history_path) if os.path.isfile(os.path.join(history_path, f)) and
         os.path.splitext(f)[1].lower() == '.json']

    def save_history(self,filename:str):
        savepath=os.path.join(history_path,filename+".json")
        print("开始保存本次对话记录...")
        with open(savepath,'w',encoding='utf-8') as fp:
            json.dump(self.history,fp,indent=4,ensure_ascii=False)
        print(f"历史对话记录已保存至:{savepath}")

    #根据输入的序号读取历史对话数据
    def load_input_num(self):
        #每个序号对应的文件名
        history_dict={str(i+1):self.save_filenames[i] for i in range(len(self.save_filenames))}
        num = input("请输入序号:")
        if num=="0":
            print("不加载历史对话，开始新对话")
            return
        elif num not in history_dict.keys():
            print("请输入正确的序号！")
            self.load_input_num()
        else:
            #选择的历史对话文件路径
            select_filepath=os.path.join(history_path,history_dict[num])
            self.load_history(select_filepath)

    def load_history(self,filepath):
        print(f"开始加载历史对话文件{filepath}...")
        with open(filepath, "r", encoding='utf-8') as fp:
            self.history = json.load(fp)
        print("加载完成！")


    #OLLAMA持续对话
    def chat_with_ollama(self):
        if len(self.save_filenames)==0:
            print("无历史记录文件，直接开始对话")
        else:
            print("读取到以下历史对话记录，输入对应序号进行加载:\n\t0:不读取")
            for i in range(len(self.save_filenames)):
                print(f"\t{i+1}:{self.save_filenames[i]}")
            self.load_input_num()  #加载历史对话记录

        print("使用说明：\n\t1.输入save保存当前对话记录\n\t2.输入exit退出对话")
        # 初始化一个列表来存储对话历史，每个元素是一个包含用户输入和模型回复的元组
        while True:
            # 获取用户输入，并转换为小写，方便后续判断退出条件
            user_input = input("\nUser: ")
            # 判断用户是否想要退出对话
            if user_input=="exit":
                break

            if user_input=="save":
                filename=input("\n请输入需要保存的文件名:")
                self.save_history(filename)
                continue

            # 将用户输入和一个空字符串（用于后续存储模型回复）作为元组添加到历史记录中
            self.history.append([user_input, ""])

            # 初始化一个列表来存储整理后的对话消息，用于请求模型生成回复
            messages = []
            # 遍历历史记录，整理对话消息
            for idx, (user_msg, model_msg) in enumerate(self.history):
                # 如果当前对话为最新的一条且未收到模型回复，则只添加用户消息
                if idx == len(self.history) - 1 and not model_msg:
                    messages.append({"role": "user", "content": user_msg})
                    break
                # 如果是用户消息，则添加到消息列表中
                if user_msg:
                    messages.append({"role": "user", "content": user_msg})
                # 如果是模型回复，则添加到消息列表中
                if model_msg:
                    messages.append({"role": "assistant", "content": model_msg})

            # 调用模型生成回复
            stream = ollama.chat(
                model=self.modelname,
                messages=messages,
                stream=True,
            )
            answer=""
            for chunk in stream:
                print(chunk['message']['content'], end='', flush=True)
                answer+=chunk['message']['content']

            # 更新history中最新用户输入的模型回复
            self.history[-1][1] = answer

if __name__ == '__main__':
    workspace_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(workspace_path)