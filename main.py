import os.path
import re
import jieba
import numpy as np
from collections import Counter
import sys


def import_text(origintextpath):
    # 函数返回值--文件内容
    textall = ''
    # 使用open函数打开对应文件
    originfile = open(origintextpath, 'r', encoding='utf-8')
    # 读取单行文本
    textline = originfile.readline()
    # 持续读取文本 直到结束
    while textline:
        textall += textline
        # 文本拼接
        textline = originfile.readline()
    return textall


# 过滤器--过滤掉符号，只剩中文
def filter_text(text):
    # 要过滤的中文符号和英语字母
    pattern = "[^\u4e00-\u9fa5]"
    # 调用re库的sub函数进行替换
    filteredtext = re.sub(pattern, '', text)
    return filteredtext


# 分词--提取出联接词汇
def extract_text(text):
    new_text = jieba.lcut(text)
    return new_text


# 进行相似度比较
def comparisonofsimilarity(str1, str2):
    # 将分词后的各个关键字进行统计个数
    co_str1 = (Counter(str1))
    co_str2 = (Counter(str2))
    p_str1 = []
    p_str2 = []
    # 统计两篇文章在这些关键字上的频率（两个数组，对应index的值对应的是相同的键）
    for temp in set(str1 + str2):
        p_str1.append(co_str1[temp])
        p_str2.append(co_str2[temp])
    # 把列表转化为数组
    p_str1 = np.array(p_str1)
    p_str2 = np.array(p_str2)
    # 余弦相似度实现
    result = p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))
    # 保留两位小数
    float_num = np.around(
        result,  # numpy数组或列表
        decimals=2  # 保留几位小数
    )
    # 数组转float
    num = np.float64(float_num).item()
    return num


# 输出
def output(result):
    # float转字符串
    str1 = str(result)
    # 获取输出路径
    c = sys.argv[3]
    # 打开文件
    openfile = open(c, 'w', encoding='utf-8')
    # 写入
    openfile.write(str1)
    # 关闭文件
    openfile.close()


# 所有调用的步骤
def main_test():
    gpus = sys.argv[1]
    batch_size = sys.argv[2]
    if not os.path.exists(gpus):
        print("原文路径不存在，请检查！")
        exit(1)
    if not os.path.exists(batch_size):
        print("抄袭文章路径不存在，请检查！")
        exit(1)
    text1 = import_text(gpus)
    text2 = import_text(batch_size)
    filtertext1 = filter_text(text1)
    filtertext2 = filter_text(text2)
    extracttext1 = extract_text(filtertext1)
    extracttext2 = extract_text(filtertext2)
    result = comparisonofsimilarity(extracttext1, extracttext2)
    output(result)
    print(result)
    return result


# 主运行
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("参数数量不符合要求！请按以下格式进行输入！")
        print("python main.py 被抄袭文章路径 抄袭文章路径 输出具体值文件路径")
        exit(1)
    main_test()
