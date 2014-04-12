Readme


Note: My update zip file includes the following item.
1.trees.py -Source Code (For it is not covenient to type in PS2-JingchengXu when call the python function so I use name trees.py instead of named PS2-JingchengXu.py)
2.PS2-Jingchengxu.txt-Answer to the question
3.PS2-Jingcheng-Xu.csv-Output for test.csv
4.tree_1.txt- The unpruned tree(For help you save time, you can read the unpruned tree directly without time consuming creating process)
5.prunetree.txt-The pruned tree

I used the python to implement the C4.5 algorithm. Including dealing with data with the following character.

a.Missing value
b.Continous
c.Sub-repalcement based Post-Pruning strategy

To test my program ,please follow the procedure.


1.Open the 'PS2JingchengXu.py' Press F5 to run the program
2.In python shell type in  'import trees'
3.type in 'reload(trees)'
4.type in 'dataSet,labels=trees.readingfile('train.csv')'
5.type in 'myTree=trees.createTree('dataSet,labels')'
Note: With a large amount of data, constructing a tree is time-consuming ,to save your time I 
have stored the tree in a txt form named 'tree_1.txt',which you could load this tree by typing 
in 'myTree=trees.grabtree('tree_1.txt')' 
6.(Optional) If you would like to see what my tree looks like just type in 'myTree', I store the 
tree in the way of nested dictionry
7.Read in validate.csv as dataSet Type in 'AccuracteRate=trees.accurateRate(myTree,dataSet,labels)' Then we will get the Accurate rate of the tree without pruning.(76.12% for this unpruning tree)
8. Type in 'PercentageAfterPruning,bestTree=trees.prune(myTree,dataSet,labels)'
  (Because we have to check every possible way of pruning in sub-replacement strategy, it is time consuming)
9. Type in 'PercentageAfterPruning' to see the percentage of accuracy after pruning
10.Type in  dataSet_test,labels_test=trees.readingfile('test.csv')
11.Type in 'testing(dataSet_test,labels_test) 
12.The result of predicting the test.csv file is output into PS2-Jingcheng-Xu.csv, you can open and check the result
