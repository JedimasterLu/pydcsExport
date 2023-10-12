import socket  			 				
import threading

host = '2.0.0.1'            # 服务器地址								
port = 8080			        # 端口					
server = socket.socket()	# 启动服务器				
server.bind((host, port))	# 设置端口和地址				
server.listen(1)		    # 设置客户端数量上限为1	

def RunServer():
    while 1:
        print("\nWait for connection...")
        conn, addr = server.accept()        # 接收客户端的数据
        print("\nconnected!")
        dataprintcnt = 0                    # 输出系数，每数次循环print一次，减少占用
        while True:	
            dataprintcnt = dataprintcnt + 1
            data = conn.recv(1024)
            data = data.decode('utf-8')
            if data == 'Quit\n':
                break

            dataList = data.splitlines()    # 输入字符串中，每个物体数据占一行，此处将物体间分开
            dataDict = {}
            for i in range(len(dataList)):
                # 循环内把每个物体的数据打包成字典，将dataList相应位置的字符串更新为相应字典
                unitLine = dataList[i]
                unitList = unitLine.split()
                dataDict['Name'] = unitList[0]
                dataDict['UnitName'] = unitList[1]
                dataDict['x'] = float(unitList[2])
                dataDict['y'] = float(unitList[3])
                dataDict["Alt"] = float(unitList[4])
                dataDict["Yaw"] = float(unitList[5]) * 57.29578
                dataDict["Pitch"] = float(unitList[6]) * 57.29578
                dataDict["Roll"] = float(unitList[7]) * 57.29578
                dataDict["vx"] = float(unitList[8])
                dataDict["vy"] = float(unitList[9])
                dataDict["vz"] = float(unitList[10])
                dataList[i] = dataDict
            # 打印含有dict的dataList看看效果
            if dataprintcnt == 300:
                print(dataList)
                dataprintcnt = 0
            
            msg = ''
            conn.send(msg)		            # 向游戏发送三个指令	
        conn.close()
        print("\ndisconnected!")

'''
# 以上为副线程，即服务器线程
threads = threading.Thread(target=RunServer,name='server',daemon=True)
threads.start()
'''