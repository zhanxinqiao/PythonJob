# -*- coding:utf-8 -*-
import joblib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
# from sklearn.externals import joblib
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
'''
    @Author     :xiaoli
    @Date       :2021/12/16
    @Description:基于K-means算法对用户信用进行分类划分
'''


class CreditCard:
    def getSourceData(self, path):
        '''
        获取数据源
        :param path:文件路径
        :return: DataFrame
        '''
        return pd.read_csv(path,encoding='unicode_escape')

    def getFeature(self, data):
        '''
        将特征数据集合降维为1
        :param data: 需要降维的数据数组
        :return: np.array
        '''
        pca = PCA(n_components=1)
        data = pca.fit_transform(data)
        return data

    def getScoreFeature(self, sourceData):
        '''
        获取降维数据获取这一系列特征值的降维特征
        :param sourceData: 源数据集合
        :return: np.array
        '''
        data = sourceData[['KnowledgeScore1', 'KnowledgeScore2', 'KnowledgeScore3']]
        return self.getFeature(data)

    def getBaseFeature(self, sourceData):
        '''
        获取降维数据获取这一系列特征值的降维特征
        :param sourceData: 源数据集合
        :return: np.array
        '''
        data = sourceData[['Genger', 'Classperformance', 'Attendance']]
        return self.getFeature(data)

    def groupPeople(self, predict, user_id):
        '''
        根据预测值与用户卡编号进行分组
        :param predict: 预测结果
        :param user_id: 用户卡编码
        :return: tuple
        '''
        res1 = []
        res2 = []
        res3 = []
        res4 = []
        res5 = []
        for i in range(len(predict)):
            if predict[i] == 0:
                res1.append(user_id[i])
            elif predict[i] == 1:
                res2.append(user_id[i])
            elif predict[i] == 2:
                res3.append(user_id[i])
            elif predict[i] == 3:
                res4.append(user_id[i])
            elif predict[i] == 4:
                res5.append(user_id[i])
        return res1, res2, res3, res4, res5

    def kMeansType(self):
        '''
                主函数
                :return:None
                '''
        # 获取源数据
        sourceData = self.getSourceData("../data/student_scores.csv")
        # 用户编号
        user_id = sourceData['StudentID']
        # 分别获取用户基本信息、课程成绩信息（每个知识点）情况降维特征
        baseFeature = self.getBaseFeature(sourceData)
        scoreFeature = self.getScoreFeature(sourceData)
        # risksFeature = self.getRisksFeature(sourceData)
        # 将二个特征合并
        allFeatures = np.append(baseFeature, scoreFeature, axis=1)  # 特征工程归一化

        # allFeatures = np.append(allFeatures, risksFeature, axis=1)#
        sdScaler = StandardScaler()
        x_data = sdScaler.fit_transform(allFeatures)
        # 初始化算法构造器，设置聚类数为7
        km = KMeans(n_clusters=7)
        # 训练数据获取模型
        model = km.fit_transform(x_data)
        # 持久化模型
        joblib.dump(model, "D:/card_km.model")
        # 获取聚类中心点
        center = km.cluster_centers_
        print("聚类的五个中心分别为：")
        for i in range(len(center)):
            print(center[i])
        # 将源数据集进行分类
        predict = km.predict(x_data)

        #res1, res2, res3, res4, res5 = self.groupPeople(predict, user_id)
        #print("*" * 20 + "以下为源数据集分类部分" + "*" * 20)
        #print("第一类：\r\n一共%d人\r\n%s" % (len(res1), str(res1[:])))
        #print("第二类：\r\n一共%d人\r\n%s" % (len(res2), str(res2[:])))
        #print("第三类：\r\n一共%d人\r\n%s" % (len(res3), str(res3[:])))
        #print("第四类：\r\n一共%d人\r\n%s" % (len(res4), str(res4[:])))
        #print("第五类：\r\n一共%d人\r\n%s" % (len(res5), str(res5[:])))
        #print("*" * 50)
        #print(x_data)
        #print(predict)
        #new_data = np.c_[x_data, predict]
        #print(new_data)
        return sourceData,predict

    def kNN_lable_ssklearn(self):
        return 1

    def kNN_Kmean_ssklearn(self):
        data,predict = self.kMeansType()
        sourceData = self.getSourceData("../data/student_scores.csv")
        # 用户编号
        user_id = sourceData['StudentID']
        # 分别获取用户基本信息、课程成绩信息（每个知识点）情况降维特征
        baseFeature  = sourceData[['Genger', 'Classperformance', 'Attendance']]
        scoreFeature = sourceData[['KnowledgeScore1', 'KnowledgeScore2', 'KnowledgeScore3']]
        # risksFeature = self.getRisksFeature(sourceData)
        # 将二个特征合并
        allFeatures = np.append(baseFeature, scoreFeature, axis=1)  # 特征工程归一化
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(allFeatures, predict, test_size=0.2)

        #clf = KNeighborsClassifier(n_neighbors=4, p=2, metric='minkowski')
        #clf.fit(Xtrain, Ytrain)
        #pre_y = clf.predict(Xtest)
        #acc = sum(pre_y == Ytest) / Xtest.shape[0]
        #print(acc)
        self.bestOfk_knn(Xtrain,Ytrain,Xtest,Ytest,10)
        self.normal_knn(Xtrain,Ytrain,Xtest,Ytest)
        return 1

    def bestOfk_knn(self,x_train, y_train, X_test, y_test, max_range):
        best_score = 0.0
        best_k = -1
        for k in range(1, max_range):
            kNN_classifier = KNeighborsClassifier(n_neighbors=k)
            kNN_classifier.fit(x_train, y_train)
            score = kNN_classifier.score(X_test, y_test)
            if score > best_score:
                best_k = k
                best_score = score
        print("best_k = ", best_k)
        print("best_score", best_score)


    def normal_knn(self,x_train, y_train, X_test, y_test):
        # 使用KNN算法,n_neighbors为k值,X_train训练数据集存入，进行拟合；X_test作为测试
        kNN_classifier = KNeighborsClassifier(n_neighbors=2)
        # 传入训练集
        kNN_classifier.fit(x_train, y_train)
        # 传入测试集，打印预测准确率
        score = kNN_classifier.score(X_test, y_test)
        print(score)
if __name__ == '__main__':
    cc = CreditCard()
    cc.kMeansType()
    cc.kNN_Kmean_ssklearn()

