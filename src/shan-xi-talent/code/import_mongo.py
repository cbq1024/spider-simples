from pymongo import MongoClient
import pandas as pd
from pymongo.errors import ConnectionFailure

# MongoDB 连接信息
username = "cxk"
password = "jntm"
host = "94.74.127.107"  # 如果是远程数据库，请替换为正确的 IP 地址或域名
port = 27017        # 默认端口，若 MongoDB 使用了不同端口，请进行调整

# MongoDB URI，带上用户名和密码进行认证
uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"

# 连接到 MongoDB
try:
    client = MongoClient(uri)
    print("MongoDB 连接成功！")
except ConnectionFailure as e:
    print(f"连接 MongoDB 失败: {e}")
    exit()

# 创建/选择数据库
db = client["job_database"]

# 创建/选择集合（相当于 SQL 中的表）
collection = db["jobs"]

# 读取 CSV 文件
csv_file_path = "jobs_data.csv"  # 请确保文件路径正确
df = pd.read_csv(csv_file_path)

# 将 pandas DataFrame 转换为字典列表
data_dict = df.to_dict(orient="records")

# 插入数据到 MongoDB 集合
try:
    collection.insert_many(data_dict)
    print("数据成功插入 MongoDB！")
except Exception as e:
    print(f"插入数据失败: {e}")

# 查询并打印所有数据，验证是否插入成功
print("插入的数据:")
for job in collection.find():
    print(job)

