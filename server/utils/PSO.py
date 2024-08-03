import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np


from app import models
from django.conf import settings
from django.core.files import File
import json
import datetime
import os
from app.consumers import Client






def get_model(path):
    train_df = pd.read_csv(path)
    X_train = train_df.iloc[:, 0:41].values
    y_train = train_df.iloc[:, 41:].values
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(41,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train[:, 0], epochs=100, batch_size=8, validation_data=(X_val, y_val[:, 0]))

    model.save_weights('model_weights.h5')
    return scaler


def objective_function(in_, scaler, model):
    # 这里是一个简单的例子，可以根据你的问题进行修改
    # model.load_weights('model_weights.h5')
    # data = [9.7152, 6.6079, 381.93697, 349.9887, 11.4552, 10.8355, 10.2232, 42.507, 9.5755, 9.3755, 9.1525, 8.8748,
    #         # 0-11
    #         8.6471, 8.3956, 8.0946, 7.7872, 7.5545, 7.296, 7.023, 6.776, 6.4635, 6.151, 5.9276, 5.6801, 14.34, 5.0475,
    #         # 12-25
    #         5.9675, 4.581, 4.331, 4.106, 16.08, 4.697, 4.34,  # 26-39
    #         ]
    # data = np.insert(data, 30, in_[0])
    # data = np.insert(data, 31, in_[1])
    # data = np.insert(data, 33, in_[2])
    # data = np.insert(data, 36, in_[3])
    # data = np.insert(data, 37, in_[4])
    # data = np.insert(data, 38, in_[5])
    # data = np.insert(data, 39, in_[6])
    # data = np.insert(data, 40, in_[7])

    input_data = np.array(in_).reshape(1, -1)
    input_data = scaler.transform(input_data)
    y_prob = model.predict(input_data, verbose=0)
    y_prob = y_prob.tolist()
    return 1 - y_prob[0][0]


class Particle:
    def __init__(self, dimension, min_, max_, scaler, model):
        self.position = [np.random.uniform(min_val, max_val) for min_val, max_val in zip(min_, max_)]
        self.position = np.array(self.position)
        self.velocity = np.random.rand(dimension)
        self.best_position = self.position
        self.best_score = objective_function(self.position, scaler, model)


def PSO(max_iter, num_particles, min_, max_, scaler, model,username):
    dimension = len(min_)
    particles = [Particle(dimension, min_, max_, scaler, model) for _ in range(num_particles)]
    global_best_position = particles[0].position  # 初始化全局最优位置
    global_best_score = objective_function(global_best_position, scaler, model)

    for i in range(max_iter):
        # print(i)

        for particle in particles:
            # 更新粒子的位置和速度
            inertia_weight = 0.725  # 惯性权重
            personal_weight = 2.0  # 个体学习因子
            social_weight = 2.0  # 群体学习因子
            r1, r2 = np.random.rand(dimension), np.random.rand(dimension)
            particle.velocity = (inertia_weight * particle.velocity +
                                 personal_weight * r1 * (particle.best_position - particle.position) +
                                 social_weight * r2 * (global_best_position - particle.position))

            # 更新粒子位置
            particle.position = np.clip(particle.position + particle.velocity, min_, max_)

            # 更新个体最优位置和全局最优位置
            current_score = objective_function(particle.position, scaler, model)
            if current_score < particle.best_score:
                particle.best_score = current_score
                particle.best_position = particle.position

            if current_score < global_best_score:
                global_best_score = current_score
                global_best_position = particle.position
        Client[username].send(json.dumps({"info":f"第{i+1}轮，loss：{str(global_best_score)[0:6]}", "type":"pso"}))

    return global_best_position, global_best_score


def run(max_iter, num_particles, min_, max_, path):
    scaler = get_model(path)
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(41,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    best_position, best_score = PSO(max_iter, num_particles, min_, max_, scaler, model)
    print("最优位置:", best_position)
    print("最优分数:", best_score)

def PSO_RUN(username,parameters,iterations):


    try:
        Client[username].send(json.dumps({
            "type":"pso",
            "info":"连接成功。",
        }))

        if ('parentId' in parameters[0]):
            del parameters[0]['parentId']
        if ('parentId' in parameters[1]):
            del parameters[1]['parentId']
        if ('id' in parameters[0]):
            del parameters[0]['id']
        if ('id' in parameters[1]):
            del parameters[1]['id']
        MAX = []
        MIN = []
        for key in parameters[0]:
            MIN.append(parameters[0][key])
            MAX.append(parameters[1][key])

        model_name = models.UserModel.objects.filter(username=username).first().model_cnn
        model_url = "%s%s"%(settings.MEDIA_ROOT,model_name)
        
        Client[username].send(json.dumps({"info":f"正在加载分类模型：{str(model_name)[19: ]}", "type":"pso"}))
        model = keras.models.load_model(model_url)
        
        Client[username].send(json.dumps({"info":"正在加载scaler...", "type":"pso"}))
        scaler = MinMaxScaler()
        scaler.fit(np.array([MIN,MAX]))


        # Client[username].send(json.dumps({"info":"正在创建优化模型...", "type":"pso"}))
        # model = keras.Sequential([
        #     layers.Dense(64, activation='relu', input_shape=(41,)),
        #     layers.Dense(32, activation='relu'),
        #     layers.Dense(2, activation='softmax')
        # ])
        # Client[username].send(json.dumps({"info":"正在编译优化模型...", "type":"pso"}))
        # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        
        Client[username].send(json.dumps({"info":"编译完成。", "type":"pso"}))
        Client[username].send(json.dumps({"info":"开始优化...", "type":"pso"}))
        best_position, best_score = PSO(iterations, 50, MIN, MAX, scaler, model,username)
        # print("最优位置:", best_position)
        # print("最优分数:", best_score)
        Client[username].send(json.dumps({"info":"优化完成。", "type":"pso"}))

        return {"finished":True,"data":best_position,"MAXMIN":[MIN,MAX]}
    
    except:
        return {"finished":False,"info":"优化过程异常中止。"}


if __name__ == '__main__':
    min_ = [3.6, 3.5, 3.38, 3.2, 0.315, 0.214, 0.151, 4.2]
    max_ = [4.1, 4.0, 3.58, 4.5, 3.092, 1.393, 0.232, 4.8]
    max_iter = 100
    num_particles = 50
    path = "train.csv"
    run(max_iter, num_particles, min_, max_, path)
