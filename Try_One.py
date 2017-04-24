# -*- coding: utf-8 -*-
import numpy as np
from numpy import *
import xml.dom.minidom
import math
from xml.etree import ElementTree as ET
from os import listdir
import operator

def createVocabList(dataSet):
    vocabSet = set([])                    #创建一个空集
    for document in dataSet:
        vocabSet = vocabSet | set(document)  #求并集
        # print(vocabSet)
    return list(vocabSet)                    #返回为列表形式

def bagOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)           #创建一个其中所含元素都为0的向量
    VecFreq = [0] * len(vocabList)
    for set in inputSet:
        for word in array(set):
            for check in vocabList:
                if word == check:
                    returnVec[vocabList.index(word)] += 1  #用到了index方法
                    VecFreq[vocabList.index(word)] += 1

    numOfdocs = len(inputSet)
    numOfshow = 0
    for word in vocabList:
        for set in inputSet:
            for check in array(set):
                if check == word:
                    numOfshow += 1
                    break
        IDF = abs(math.log(numOfdocs/(numOfshow+1),10))
        returnVec[vocabList.index(word)] *= IDF
        numOfshow = 0
    return returnVec,VecFreq

'''
@brief  应该用哈希表改进....
@:param document 文件名
@:return myVocabList 所有关键词
@:return Vec 所有关键词对应的词频
@:return TopKeyWords 词频前X的关键词
'''
def createKeywords(document):
    dom = xml.dom.minidom.parse(document)
    root = dom.documentElement

    itemlist = root.getElementsByTagName('KeyWords') #获得的是KeyWords的一组标签
    keyWordLists = []
    for item in itemlist:
        keywords = item.firstChild.data
        word = keywords.split(';')
        keyWordLists.append(word)

    myVocabList = createVocabList(keyWordLists)  #关键词汇库

    Vec,VecFreq = bagOfWords2Vec(myVocabList,keyWordLists) #词袋模型 TF-IDF模型
    ReverseVec = sorted(Vec,reverse = True)
    TempReverseVec = set([])
    for index in ReverseVec:
        TempReverseVec = TempReverseVec | set([index])
    FinalReverseVec = list(TempReverseVec)
    FinalReverseVec = sorted(FinalReverseVec,reverse = True)

    print FinalReverseVec

    TopKeyWords = []
    TopKeyWordsIndex = []
    TopKeyFreq = []

    number = 0
    for item in FinalReverseVec:
        if item>=20:     #TF-IDF超过多少为Keyword
            number+=1

    for i in range(0,number):  #可优化
        for j in range(0,len(Vec)):
            if Vec[j] == FinalReverseVec[i]:
                TopKeyWordsIndex.append(j)

    for i in range(0,len(TopKeyWordsIndex)):
        TopKeyWords.append(myVocabList[TopKeyWordsIndex[i]])
        TopKeyFreq.append(VecFreq[TopKeyWordsIndex[i]])


    return myVocabList,Vec,TopKeyWords,TopKeyFreq

def calculate(keyword_1,keywordFreq_1,TopKeyword_1,TopKeywordFreq_1,
              keyword_2, keywordFreq_2, TopKeyword_2, TopKeywordFreq_2):
    finalKeyword = []
    Freq_1 = []
    Freq_2 = []

    for item_1 in TopKeyword_1:
        equalFlag = 0
        for item_2 in TopKeyword_2:
            if item_1 == item_2:
                finalKeyword.append(item_1)
                Freq_1.append(TopKeywordFreq_1[TopKeyword_1.index(item_1)])
                Freq_2.append(TopKeywordFreq_2[TopKeyword_2.index(item_2)])
                equalFlag = 1
                break

        if equalFlag == 0:
            finalKeyword.append(item_1)
            Freq_1.append(TopKeywordFreq_1[TopKeyword_1.index(item_1)])
            Freq_2.append(0)


    for item_2 in TopKeyword_2:
        flag = 0
        for item_1 in TopKeyword_1:
            if item_1 == item_2:
                flag = 1
                break
        if flag == 0:
            finalKeyword.append(item_2)
            Freq_2.append(TopKeywordFreq_2[TopKeyword_2.index(item_2)])
            Freq_1.append(0)

    for i in range(len(finalKeyword)):
        print "%s      %d       %d" %(finalKeyword[i],Freq_1[i],Freq_2[i])

    vector_1 = np.array(Freq_1)
    vector_2 = np.array(Freq_2)

    length_1 = np.sqrt(vector_1.dot(vector_1))
    length_2 = np.sqrt(vector_2.dot(vector_2))
    print "length of vector_1 is %f" % length_1
    print "length of vector_2 is %f" % length_2
    cos_angle = vector_1.dot(vector_2) / (length_1 * length_2)
    return cos_angle


keyword_1,keywordFreq_1,TopKeyword_1,TopKeywordFreq_1 = createKeywords('20161123/美国1000.xml')
keyword_2,keywordFreq_2,TopKeyword_2,TopKeywordFreq_2 = createKeywords('20161123/国内1000.xml')


cos = calculate(keyword_1,keywordFreq_1,TopKeyword_1,TopKeywordFreq_1,
          keyword_2, keywordFreq_2, TopKeyword_2, TopKeywordFreq_2)
print "the cos value is %f" %cos

