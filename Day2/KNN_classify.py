'''
Author: LZC
Date: 2022-02-25 21:17:29
LastEditTime: 2022-02-27 10:44:34
Description: file content
FilePath: \k近邻分类算法\KNN_classify.py
'''
import numpy as np
# import sklearn
from sklearn import datasets
from sklearn import model_selection
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


COLOR = ['red', 'green', 'blue']
cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
h = 1


# 将每一类属性分类
def show_scattor(data, target, label, i):

    x = range(len(data[:, i]))

    clf = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
    clf.fit(np.c_[x, data[:, i]], target)

    plt.title(label[i])

    x_min, x_max = data[:, i].min(), data[:, i].max()

    xx = np.array(x)
    yy = np.linspace(x_min, x_max, len(target))

    xx, yy = np.meshgrid(xx, yy)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    # 根据边界填充颜色
    Z = Z.reshape(xx.shape)

    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    for t in range(len(x)):
        plt.scatter(x[t], data[t, i], color=COLOR[target[t]])

    plt.show()


# 对数据降维显示后的数据分类
def show_pca_scattor(data, target):

    pca = PCA(n_components=3)

    new_data = pca.fit_transform(data)

    fig = plt.figure()
    ax = Axes3D(fig)

    for i in range(len(target)):
        ax.scatter3D(new_data[i, 0], new_data[i, 1],
                     new_data[i, 2], color=COLOR[target[i]])
    plt.show()


if __name__ == '__main__':

    # download dataset
    iris = datasets.load_iris()

    # get data from dataset
    x = iris.data
    y = iris.target
    label = iris.feature_names
    # print(x, y, label)
    # print(x[:, 0])

    # show_scattor(x, y, label, 0)
    # show_scattor(x, y, label, 1)
    # show_scattor(x, y, label, 2)
    # show_scattor(x, y, label, 3)

    show_pca_scattor(x, y)

    # show iris features and values
    df = pd.DataFrame(x, columns=label)
    # print(df[:5])

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(x, y, test_size=0.2)

    # show test of dataset
    # print(Xtest, Ytest)

    clf = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
    clf.fit(Xtrain, Ytrain)

    pre_y = clf.predict(Xtest)
    acc = sum(pre_y == Ytest)/Xtest.shape[0]
    print(acc)
