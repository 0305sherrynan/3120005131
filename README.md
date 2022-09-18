
@[TOC](这里写目录标题)
# 1、项目地址
[github](https://github.com/0305sherrynan/3120005131)

---
# 2、PSP表格
| PSP2.1|Personal Software Process Stages|预估耗时（分钟）|实际耗时（分钟） |
| :-----| :---- |:---- | :----|
| Planning|计划 | 30|20
|  · Estimate|· 估计这个任务需要多少时间| 10|15
|Development|开发|120|240
|· Analysis|· 需求分析 (包括学习新技术)|30|50
|· Design Spec|· 生成设计文档|20|15
|· Design Review|· 设计复审|15|10
|· Coding Standard|· 代码规范 (为目前的开发制定合适的规范)|10|7
|· Design|· 具体设计|20|30
|· Coding|· 具体编码|20|30
|· Code Review|· 代码复审|10|10
|· Test|· 测试（自我测试，修改代码，提交修改）|70|120
|Reporting|报告|40|30
|· Test Repor|· 测试报告|40|20
|· Size Measurement|· 计算工作量|30|30
|· Postmortem & Process Improvement Plan|· 事后总结, 并提出过程改进计划|10|10
||	· 合计|475|637

---
# 3、各模块设计与实现过程
## 3.1、思路分析
 首先明确目标是对中文文章进行查重，而中文不像英文，以每个空格隔开两个单词，中文有词语和成语等，由此我们需要借助第三方中文分词库；之后便是相似度算法的实现。具体为：文件内容导入->过滤->分词->相似度比较->导出具体值。

---
## 3.2、模块设计与实现
### 3.2.1、模块分类
我们以上述思路为基准，
- 主运行（if __name__ == '__main__':）进行各个模块的实现；
- import_text()：将需要比较查重的文件内容导入并读取；
- filter_text(text)：作为过滤器--过滤掉特殊字符，只剩下中文字符；
- extract_text(text)：是分词--提取出联接词汇；
- Comparison0fSimilarity(str1,str2)：进行相似度比较。
- ---
### 3.2.2、具体实现思维导图![在这里插入图片描述](https://img-blog.csdnimg.cn/650b0dc5f931468dae10429fb12d81d1.png#pic_center)
---
### 3.2.3、关键模块的实现
#### 分词
常用的分词库有：jieba分词、哈工大LTP和中科大NLPIR
这里仅是实现一个查重小demo，所以我们选择上手简单且简洁的jieba分词

---
#### 相似度比较--使用余弦相似度算法
- 算法
![在这里插入图片描述](https://img-blog.csdnimg.cn/98f3ebffac7840b2bea24b45e2de3d4b.png#pic_center)
- 流程图

![在这里插入图片描述](https://img-blog.csdnimg.cn/16c755eb8aa44aa7a8e6c3ff24136291.png#pic_center)
- 实现关键
 1、 两个列表分别进行统计个数，用到内置的Counter函数，方便快速进行统计；
 2、统计两篇文章在这些关键字上的频率，首先不能直接进行拼接，因为有共同的关键字，这样会拉低效率，使用set函数，将重复的关键字去除；
 3、最后调用numpy库，将列表转数组，进行向量内积，得到最终结果。

---
 # 4、性能改进
 ## 4.1、性能分析图
 使用gprof2dot+cProfile库进行性能分析
 参考文章：
 - [https://www.pianshen.com/article/41831302762/](https://www.pianshen.com/article/41831302762/)
 - [https://zhuanlan.zhihu.com/p/24495603](https://zhuanlan.zhihu.com/p/24495603)
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/16624378db74450f9e957f083f7e2bf4.png#pic_center)

---
## 4.2、各函数运行占用时间--使用line_profiler第三方库
- 导入数据：import_text()

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/a7c20e99973a4d68adbc92b0f225f711.png#pic_center)

- 过滤字符：filter_text(text)
![在这里插入图片描述](https://img-blog.csdnimg.cn/9f1624adf6fe4701be39f3226094a6f5.png#pic_center)

- 分词：extract_text(text)

![在这里插入图片描述](https://img-blog.csdnimg.cn/3a03846b566e4b71aedd407978c071c5.png#pic_center)
- 相似度比较：Comparison0fSimilarity(str1,str2)
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/6285577e7e674dd686155cc9b911fc3e.png#pic_center)
可以看到导入模块耗时高，但是是由于此处是用户输入路径，所以有中间停顿时间，故不计入考虑；所以最高的是extract_text(text)函数中调用jieba库的函数lcut，但由于是亦封装好的函数，所以无法进行优化。

---
# 5、模块单元测试
## 5.1、对关键模块--“相似度比较”进行单元测试
- unit_text.py 代码编写--使用pycharm当中自动生成的测试单元代码，import 要测试的函数main，并在断言函数里引入要测试的具体函数模块，如此处的ComparisonOfSimilarity，并传入测试参数。

```python
import unittest
import main

class MyTestCase(unittest.TestCase):
    def test_something(self):
         self.assertEqual(main.Comparison0fSimilarity(['今天', '天气', '真', '挺好', '的'],
        ['今天', '气候', '真', '挺不错', '的', ]), 0.6) # add assertion here
        #self.assertEqual(main.Comparison0fSimilarity(['今天', '天气', '真', '挺好', '的'],
        #['今天', '气候', '真', '挺不错', '的', ]), 0.4) # assert example 2

if __name__ == '__main__':
    unittest.main()

```
- 通过余弦相似度算法计算并保留两位小数得到的答案为0.60，我们断言为0.6，得到结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/5137a75aedc74485ada4a863d1b50829.png#pic_center)
- 我们断言为0.4，得到结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/3a5f239af7af4ed098de06fdb468dc54.png#pic_center)

---
## 5.2、 覆盖率测试
- 使用第三方库coverage进行测试
![在这里插入图片描述](https://img-blog.csdnimg.cn/3d342cf6928c4eeba8653c86bc754eaa.png#pic_center)

- 可以看到覆盖率很好。

![在这里插入图片描述](https://img-blog.csdnimg.cn/22a26c366d534c7ab9a0b69d18b3da1d.png#pic_center)

---
# 6、异常处理
## 6.1、变量名大小写问题和模块间距问题
由于第一次使用python，对变量和模块间距的书写不规范，所以导致警告。解决方法：按照要求将大写的改为小写，间距改为两行。
![在这里插入图片描述](https://img-blog.csdnimg.cn/9f785083e0214938b7a5fb882b92204e.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/d82b92d6dcb2431e9e23f5790cc6e723.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/82a58e124852432a9703d17bbf84d56b.png#pic_center)

---
## 6.2、命令行执行代码参数不足
由于要求在命令行执行函数并传入参数，所以会存在参数与所需要的不匹配，如本次项目需要传入四个参数：执行文件名 被抄袭文件名 抄袭文件名 输出文件名。并且我们用到内置的sys模块进行参数的获取，所以我们只需要在函数开始的时候判断sys里面argv的个数是否满足需求即可。
```python
if __name__ == '__main__':
    if len(sys.argv) != 4 :
        print("参数数量不符合要求！请按以下格式进行输入！")
        print("python main.py 被抄袭文章路径 抄袭文章路径 输出具体值文件路径")
        exit(1)
    main_test()
```
测试--少输入一个参数：
![在这里插入图片描述](https://img-blog.csdnimg.cn/25591d5ac6e545edb1d55688011fa337.png#pic_center)

---
## 6.3、只读文件不存在
输出文件是写文件，不存在可以自动生成，但是两个源文件是必须要存在的，所以路径一定要正确。

```python
def main_test():
    gpus = sys.argv[1]
    batch_size = sys.argv[2]
    if not os.path.exists(gpus):
        print("原文路径不存在，请检查！")
        exit(1)
    if not os.path.exists(batch_size):
        print("抄袭文章路径不存在，请检查！")
        exit(1)
```

测试
![在这里插入图片描述](https://img-blog.csdnimg.cn/ea6a05e08027494e930cdf806e071559.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/840626ffba7f46f7a3ee7af7fa630b3f.png#pic_center)

----
# 7、测试用例
`备注：为方便运行，命令行参数写在pycharm的“编辑配置”中`
![在这里插入图片描述](https://img-blog.csdnimg.cn/6d26500c384d4169a8782853137f20fa.png#pic_center)
- 用例1、python main.py C:\wenjian\orig.txt C:\wenjian\orig_0.8_add.txt C:\wenjian\answer.txt![在这里插入图片描述](https://img-blog.csdnimg.cn/3e3720769ce14e2e9c242ce925ed3988.png#pic_center)


- 用例2、python main.py C:\wenjian\orig.txt C:\wenjian\orig_0.8_del.txt C:\wenjian\answer.txt
![在这里插入图片描述](https://img-blog.csdnimg.cn/faf65b8f0830475bbae966d127464bee.png#pic_center)
- 用例3、python main.py C:\wenjian\orig.txt C:\wenjian\orig_0.8_dis_1.txt C:\wenjian\answer.txt
![在这里插入图片描述](https://img-blog.csdnimg.cn/b026a2fff31f4103ad2a33f7efd96e1f.png#pic_center)
- 用例4、python main.py C:\wenjian\orig.txt C:\wenjian\orig_0.8_dis_10.txt C:\wenjian\answer.txt
![在这里插入图片描述](https://img-blog.csdnimg.cn/b28674fb05134374976108a5d008f754.png#pic_center)
- 用例5、python main.py C:\wenjian\orig.txt C:\wenjian\orig_0.8_dis_15.txt C:\wenjian\answer.txt
![在这里插入图片描述](https://img-blog.csdnimg.cn/f83f04e331294866b5453c28c11bd9c8.png#pic_center)
