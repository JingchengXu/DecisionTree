from math import log
from operator import itemgetter,attrgetter
import operator
import types
import csv
import numpy
import math
import sys
import copy
def readingfile(filename):
    with open(filename,'rb')as csvfile:
        dataSet=[]
        labels=[]
        reader=csv.reader(csvfile)
        for row in reader:
            dataSet.append(row)
        labels=dataSet[0]
        del dataSet[0]
        numfeature=len(dataSet[0])-1
        for m in range(numfeature):
            largesttemp=0
            featList=[testVec[m] for testVec in dataSet]
            unival=set(featList)
            for value in unival:
                if value!='?':
                    temp=featList.count(value)
                    if temp>largesttemp:
                        largesttemp=temp
                        setvalue=value
            for n in range(len(dataSet)):
                if dataSet[n][m]=='?':
                    dataSet[n][m]=setvalue
                
            
        for i in range(0,3):
            for j in range(0,len(dataSet)):
                dataSet[j][i]=int (dataSet[j][i])
        for i in range(5,12):
            for j in range(0,len(dataSet)):
                dataSet[j][i]=int (dataSet[j][i])
        for j in range(0,len(dataSet)):
            if dataSet[j][12]!='?':
                dataSet[j][12]=int(dataSet[j][12])
        return dataSet,labels
def storeTree(myTree,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(myTree,fw)
    fw.close()

def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet_number(dataSet,axis,j):
    small=dataSet[:j+1]
    big=dataSet[j+1:]
    mean=float(dataSet[j][axis]+dataSet[j+1][axis])/2
      
    return small,big,mean
def splitDataSet_string(dataSet,axis,value):
    ret=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            ret.append(featVec)
    return ret

def chooseBestFeatureToSplit(dataSet,baseEntropy):
    numFeatures=len(dataSet[0])-1    
    bestInfoGain=0.0;
  #  print baseEntropy
    bestFeature=-1
    bestpoint=0
    best_small=[]
    best_big=[]
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
  #      print uniqueVals
        newEntropy=0.0
        if type(featList[0])==type(1):
            temp=sorted(dataSet,key=itemgetter(i))
            length=len(temp)
            for j in range (0,length-1):
                if temp[j][-1]!=temp[j+1][-1]:
                    small,big,point=splitDataSet_number(temp,i,j)
                    prob_1=len(small)/float(len(dataSet))
                    prob_2=len(big)/float(len(dataSet))
                    newEntropy=prob_1*calcShannonEnt(small)+prob_2*calcShannonEnt(big)
                    infoGain=baseEntropy-newEntropy
                    if(infoGain>bestInfoGain):
                        bestInfoGain=infoGain
                        bestFeature=i
                        bestpoint=point
                        best_small=small
                        best_big=big
                            
        if type(featList[0])!=type(1):
            newEntropy=0
            for value in uniqueVals:
                ret=splitDataSet_string(dataSet,i,value)
                prob=len(ret)/float(len(dataSet))
                newEntropy+=prob*calcShannonEnt(ret)
            infoGain=baseEntropy-newEntropy
            if(infoGain>bestInfoGain):
                bestInfoGain=infoGain
                bestFeature=i

    return bestFeature,bestpoint,best_small,best_big

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    data=[]
    baseEntropy=calcShannonEnt(dataSet)
    if classList.count(classList[0])==len(classList):
        #print classList[0]
        return classList[0]
    if len(dataSet[0])==1:
   #     print majorityCnt(dataSet)
        return majorityCnt(dataSet)
    bestFeat,bestpoint,best_small,best_big=chooseBestFeatureToSplit(dataSet,baseEntropy)
    bestFeatLabel=labels[bestFeat]
    #print bestFeatLabel
    myTree={bestFeatLabel:{}}
    featValues=[example[bestFeat] for example in dataSet]
    if type(featValues[0])!=type(1):
        uniqueVals=set(featValues)
        for value in uniqueVals:
            subLabels=labels[:]
            #print value
            myTree[bestFeatLabel][value]=createTree(splitDataSet_string(dataSet,bestFeat,value),subLabels)
    if type(featValues[0])==type(1):
        data=[best_small,best_big]
        bestpoint_print=str(bestpoint)
        label=['<'+bestpoint_print,'>'+bestpoint_print]
        for i in range(0,2):
            subLabels=labels[:]       
            myTree[bestFeatLabel][label[i]]=createTree(data[i],subLabels)    
    return myTree
def grabtree(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)

def classify(myTree,featLabels,testVec,count):
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    featIndex=featLabels.index(firstStr)
    if type(secondDict).__name__=='dict':
        for key in secondDict.keys():
            if key.isalpha()==True:
                if testVec[featIndex]==key:
                    if type(secondDict[key]).__name__=='dict':
                         #print key
                        classify(secondDict[key],featLabels,testVec,count)
                    else:
                        if testVec[-1]==secondDict[key]:
                            count.extend('1')                        
                        else:
                            count=count
            if key.isalpha()==False:
                if key[0]=='<':
                    key_1=key[1:]
                    Num=float(key_1)
                    if testVec[featIndex]<=Num:
                        key_test='<'+key_1
                        if type(secondDict[key_test]).__name__=='dict':
                        #print key_test
                            classify(secondDict[key_test],featLabels,testVec,count)
                        else:
                            if testVec[-1]==secondDict[key_test]:
                                count=count.extend('1')
                            
                            
                            else:
                                count=count
                    if testVec[featIndex]>Num:
                        key_test='>'+key_1
                        if type(secondDict[key_test]).__name__=='dict':
                        #print key_test
                            classify(secondDict[key_test],featLabels,testVec,count)
                        else:
                            if testVec[-1]==secondDict[key_test]:
                                count=count.extend('1')
                            
                            else:
                                count=count
    return count
def getNumLeafs(myTree):
    numLeafs=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else: numLeafs+=1
    return numLeafs
def getTreeDepth(myTree):
    maxDepth=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondDict[key])
        else: thisDepth=1
        if thisDepth>maxDepth: maxDepth=thisDepth
    return maxDepth
                


def accurateRate(myTree,dataSet,labels):
   # import pickle
   # fr=open('tree_1.txt')
   # myTree=pickle.load(fr)
    count=[]
    for testVec in dataSet:
        temp=classify(myTree,labels,testVec,count)
 #   print count
    accurateRate=float(len(count))/len(dataSet)
    percentage=accurateRate*100
    output=str(percentage)
    #print 'The accuracy is '+output+'%'
    return percentage
def get_pathes(the_model):
    pathes = []
    def prune_model(model, path):
        if (type(model) is dict):
            for key in model.keys():
                path.append(key)
                prune_model(model[key], copy.deepcopy(path))
                path.remove(key)
        else:
            path.pop(len(path)-1)
            pathes.append(path)
            return
    prune_model(the_model, [])
    return pathes

def get_disjunctive(the_model):
    pathes = []
    def prune_model(model, path):
        if (type(model) is dict):
            for key in model.keys():
                path.append(key)
                prune_model(model[key], copy.deepcopy(path))
                path.remove(key)
        else:
            #path.pop(len(path)-1)
            pathes.append(path)
            return
    prune_model(the_model, [])
    return pathes
def postcondition(model,path):
    if (len(path) == 0):
        model = 1
        return
    while (len(path) > 1):     
        key = path.pop(0)
        if key in model.keys():
            model = model[key]
        else:
            break
    key = path.pop(0)
    if key in model.keys():
        print model[key]

def unique_pathes(path_list):
    unique_box = []
    for path in path_list:
        label = 0
        if (path == []):
            continue
        for item in unique_box:
            if (path == item):
                label = 1
                break
        if (label == 1):
            continue
        else:
            unique_box.append(path)
    return unique_box

def replace_subtree_1(model,path):
    if (len(path) == 0):
        model = 1
        return
    while (len(path) > 1):     
        key = path.pop(0)
        if key in model.keys():
            model = model[key]
        else:
            break
    key = path.pop(0)
    if key in model.keys():
        model[key] = 1
    

def replace_subtree_0(model,path):
    if (len(path) == 0):
        model = 1
        return
    while (len(path) > 1):     
        key = path.pop(0)
        if key in model.keys():
            model = model[key]
        else:
            break
    key = path.pop(0)
    if key in model.keys():
        model[key] = 0
    
def prune(myTree,dataSet,labels):
    bestpercentage=76.12
    pathes=get_pathes(myTree)
    unique_box=unique_pathes(pathes)
    percentage_1=0
    percentage_2=0
    for path in unique_box:
        #print path
        #print (accurateRate(myTree,dataSet,labels))
        Zero=copy.deepcopy(myTree)
        replace_subtree_0(Zero,path)
        percentage_1=accurateRate(Zero,dataSet,labels)
       # print percentage_1
        One=copy.deepcopy(myTree)
        replace_subtree_1(One,path)
        percentage_2=accurateRate(One,dataSet,labels)
       # print percentage_2
        if percentage_1>percentage_2 and percentage_1>bestpercentage:
            bestpercentage=percentage_1
            bestTree=Zero
        if percentage_2>percentage_1 and percentage_2>bestpercentage:
            bestpercentage=percentage_2
            bestTree=One
    return bestpercentage,bestTree
def testing (dataSet,labels):
   
    import pickle
    fr=open('tree_1.txt')
    myTree=pickle.load(fr)
    with open('PS2-Jingcheng-Xu.csv','wb') as result:
        file_writer=csv.writer(result)        
        file_writer.writerow([Temp for Temp in labels])
        for testVec in dataSet:
            classify_test(myTree,labels,testVec)
            file_writer.writerow([Temp_1 for Temp_1 in testVec])
       
            
def classify_test(myTree,featLabels,testVec):
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    featIndex=featLabels.index(firstStr)
    if type(secondDict).__name__=='dict':
        for key in secondDict.keys():
            if key.isalpha()==True:
                if testVec[featIndex]==key:
                    if type(secondDict[key]).__name__=='dict':
                         #print key
                        classify_test(secondDict[key],featLabels,testVec)
                    else:
                        if secondDict[key]==0 or secondDict[key]==1:
                            testVec.append(secondDict[key])
                        else:
                            testVec.append(1)
                  
            if key.isalpha()==False:
                if key[0]=='<':
                    key_1=key[1:]
                    Num=float(key_1)
                    if testVec[featIndex]<=Num:
                        key_test='<'+key_1
                        if type(secondDict[key_test]).__name__=='dict':
                        #print key_test
                            classify_test(secondDict[key_test],featLabels,testVec)
                        else:
                            if secondDict[key]==0 or secondDict[key]==1:
                                testVec.append(secondDict[key])
                            else:
                                testVec.append(1)
                    if testVec[featIndex]>Num:
                        key_test='>'+key_1
                        if type(secondDict[key_test]).__name__=='dict':
                        #print key_test
                            classify_test(secondDict[key_test],featLabels,testVec)
                        else:
                            if secondDict[key]==0 or secondDict[key]==1:
                                testVec.append(secondDict[key])
                            else:
                                testVec.append(1)
