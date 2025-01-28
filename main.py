from utils.ollama_func import OLLAMA
if __name__ == '__main__':
    ollama_class=OLLAMA('deepseek-r1:32b')
    ollama_class.chat_with_ollama()