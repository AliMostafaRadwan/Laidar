import random

from rplidar import RPLidar
import numpy as np
import cv2
import math
import time
import keyboard
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

lidar = RPLidar('COM5')

info = lidar.get_info()
health = lidar.get_health()
rancolor = {}
try:
    for i, scan in enumerate(lidar.iter_scans('express')):
        df = pd.DataFrame(columns=('x', 'y'))
        img = np.zeros((1000, 1000, 3), np.uint8)
        print('%d: Got %d measurments' % (i, len(scan)))
        if(i%2 == 0):
            for l,(j, r, d) in enumerate(scan):
                if(d < 2000):
                    d = d*0.3
                    r = math.radians(r)
                    x = int(d*math.cos(r))
                    y = int(d*math.sin(r))
                    df.loc[l] = [x,y]
                    # cv2.line(img, (250,250),(x+250,y+250), (255,0,0),1)
            #K-means로 군집화 결정하는 것
            # data_points = df.values
            # kmeans = KMeans(n_clusters=3).fit(data_points)
            # df['cluster_id'] = kmeans.labels_
            #DBSCAN으로 군집 결정
            db_scan = DBSCAN(eps=20, min_samples=3).fit(df.values)
            df['cluster_id'] = db_scan.labels_
            print(df[100:])
            for column_name, row in df.iterrows():
                if row[2] == -1:
                    k = (255, 255, 255)
                    cv2.line(img, (row[0] + 500, row[1] + 500), (row[0] + 500, row[1] + 500), k, 3)
                    continue
                if row[2] not in rancolor:
                    rancolor[row[2]] = (100+random.randrange(1,150),100+random.randrange(1,150),100+random.randrange(1,150))
                # if(row[2] == 1):
                #     k = (255, 0, 0)
                # elif(row[2] == 2):
                #     k = (0, 255, 0)
                # elif (row[2] == -1):
                #     print(row)
                #     k = (255, 255, 255)
                # elif (row[2] == 3):
                #     k = (0, 255, 255)
                # else:
                #     k = (0, 0, 255)
                cv2.line(img, (row[0] + 500, row[1] + 500), (row[0] + 500, row[1] + 500), rancolor[row[2]], 3)
            # h, w = img.shape[:2]
            # print(type(img))
            # lines = cv2.HoughLines(img, 1, np.pi/180,3)
            # print("여기까지됨")
            # for line in lines:  # 검출된 모든 선 순회
            #     r, theta = line[0]  # 거리와 각도
            #     tx, ty = np.cos(theta), np.sin(theta)  # x, y축에 대한 삼각비
            #     x0, y0 = tx * r, ty * r  # x, y 기준(절편) 좌표
            #     # 기준 좌표에 빨강색 점 그리기
            #     cv2.circle(img, (abs(x0), abs(y0)), 3, (0, 0, 255), -1)
            #     # 직선 방정식으로 그리기 위한 시작점, 끝점 계산
            #     x1, y1 = int(x0 + w * (-ty)), int(y0 + h * tx)
            #     x2, y2 = int(x0 - w * (-ty)), int(y0 - h * tx)
            #     # 선그리기
            #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.imshow('image', img)

        if cv2.waitKey(1) == ord('q'):  # q를 누르면 종료
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            cv2.destroyAllWindows()
            print("멈춰!")
            break
except:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    cv2.destroyAllWindows()