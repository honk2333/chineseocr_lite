# coding: utf-8
import cmd
import os
import pypinyin
import re
from openccpy.opencc import *

# 存放敏感词文件的路径
filtered_words_filepath = 'key/'
class CLI(cmd.Cmd):
    def __init__(self):  # 初始基础类方法
        cmd.Cmd.__init__(self)  # 初始化，提取敏感词列表
        self.intro = 'Python敏感词检测:'  # 输出欢迎信息
        files = os.listdir(filtered_words_filepath)
        self.words = []
        for file in files:
            with open('key/' + file, 'r', encoding='utf-8') as fp:
                word = fp.read().split('\n')
                print("词库({})敏感词的数目：{}".format(file, len(word)))
                self.words += word
        self.words = set(self.words)
        self.prompt = ">>> "  # 定义提示符

    def default(self, line):
        # 去除标点符号
        line = re.sub('\W+', '', line).replace('_', '')
        # 繁体字转换成中文
        tmp = ""
        for word in list(line):
            tmp += Opencc.to_simple(word)
        line = tmp
        # 一、直接包含违规词
        detected = [i for i in self.words if i in line]
        if any(detected):
            print('和谐，检测到违规词为：{}'.format(" ".join(detected)))
            return

        # 二、包含违规拼音
        # 1，如果原本的违规词是汉字形式，主要是为了匹配同音词的情况
        # 误判率太高，例如读博==赌博？，暂定
        # pinyin_line = pypinyin.lazy_pinyin(line)
        # pinyin_line = " ".join(pinyin_line)
        # if any([" ".join(pypinyin.lazy_pinyin(i)) in pinyin_line for i in self.words]):
        #     print('和谐')
        # 2，如果原本的违规词就是拼音形式
        # 加速方式，先判断输入中是否含有拼音，避免遍历词库
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, line)
        # 如果包含字母，进一步检测是否有违规拼音
        if len(res) != 0:
            detected = [i for i in self.words if len(i) > 1 and "".join(pypinyin.lazy_pinyin(i)) in line.lower()]
            if any(detected):
                print('和谐，检测到违规词为：{}'.format(" ".join(detected)))
                return

        print('不和谐')
        return

    def do_quit(self, arg):
        exit()
        return True
        

class TextFilter():
    def __init__(self):  # 初始基础类方法
        # 载入敏感词库
        files = os.listdir(filtered_words_filepath)
        self.words = []
        for file in files:
            with open('key/' + file, 'r', encoding='utf-8') as fp:
                word = fp.read().split('\n')
                # print("词库({})敏感词的数目：{}".format(file, len(word)))
                self.words += word
        self.words = set(self.words)

    def Filter(self, line):
        # 去除标点符号
        line = re.sub('\W+', '', line).replace('_', '')
        # 繁体字转换成中文
        tmp = ""
        for word in list(line):
            tmp += Opencc.to_simple(word)
        line = tmp
        # 一、直接包含违规词
        detected = [i for i in self.words if i in line]
        res = ''
        if any(detected):
            res = '和谐，检测到违规词为：{}'.format(" ".join(detected))
            return res

        # 二、包含违规拼音
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, line)
        # 如果包含字母，进一步检测是否有违规拼音
        if len(res) != 0:
            detected = [i for i in self.words if len(i) > 1 and "".join(pypinyin.lazy_pinyin(i)) in line.lower()]
            if any(detected):
                res = '和谐，检测到违规词为：{}'.format(" ".join(detected))
                return res

        res = '不和谐'
        return res


if __name__ == "__main__":
    cli = CLI()
    cli.cmdloop()
