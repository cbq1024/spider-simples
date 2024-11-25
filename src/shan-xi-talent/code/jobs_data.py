import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import re

# 输入文件路径，包含公司名称和ID
input_file = "jobs_info.csv"  # 文件内容示例：山西国创科技有限责任公司,1068961

# 输出文件路径
output_file = "jobs_data.csv"

# 模拟请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 读取公司名称和 ID
companies = []
with open(input_file, mode="r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 2:
            companies.append((parts[0], parts[1]))

# 准备CSV文件
with open(output_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # 写入CSV头部
    writer.writerow(["Company ID", "Company Name", "Job Title", "Hiring Count", "Job Type", "Posted Time", "Salary", "Location", "Experience", "Education"])

    # 遍历每家公司
    for company_name, company_id in companies:
        # 设置目标 URL
        url = f"https://sjrc.com.cn/index.php?m=&c=jobs&a=com_jobs_list&id={company_id}"

        # 发起请求
        response = requests.get(url, headers=headers, verify=False)

        # 检查请求状态
        if response.status_code == 200:
            # 解析HTML
            soup = BeautifulSoup(response.text, "lxml")

            # 找到目标 div
            ajax_list = soup.find("div", class_="ajax-list")
            jobs_list = ajax_list.find_all("div", class_="jobslist J_jobsList") if ajax_list else []

            # 遍历所有职位
            for job in jobs_list:
                # 提取职位名称、人数、类型、发布时间
                jname_div = job.find("div", class_="jname")
                job_title = jname_div.find("a").get_text(strip=True)
                hiring_count = jname_div.find_all("span")[0].get_text(strip=True)
                job_type = jname_div.find_all("span")[1].get_text(strip=True)
                posted_time_raw = jname_div.find_all("span")[2].get_text(strip=True)

                # 处理发布时间，转换为标准日期格式（包含时分秒）
                posted_time = posted_time_raw
                try:
                    # 判断发布时间的格式并进行处理
                    if "分钟前" in posted_time_raw:
                        minutes_ago = int(re.search(r"(\d+)分钟前", posted_time_raw).group(1))
                        posted_time = (datetime.now() - timedelta(minutes=minutes_ago)).strftime("%Y年%m月%d日 %H:%M:%S")
                    elif "刚刚" in posted_time_raw:
                        posted_time = (datetime.now()).strftime("%Y年%m月%d日 %H:%M:%S")
                    elif "小时前" in posted_time_raw:
                        hours_ago = int(re.search(r"(\d+)小时前", posted_time_raw).group(1))
                        posted_time = (datetime.now() - timedelta(hours=hours_ago)).strftime("%Y年%m月%d日 %H:%M:%S")
                    elif "天前" in posted_time_raw:
                        days_ago = int(re.search(r"(\d+)天前", posted_time_raw).group(1))
                        posted_time = (datetime.now() - timedelta(days=days_ago)).strftime("%Y年%m月%d日 %H:%M:%S")
                except Exception as e:
                    print(f"处理发布时间时发生错误: {e}, 保留原始值: {posted_time_raw}")

                # 提取薪资、地点、经验、学历要求
                jtxt_div = job.find("div", class_="jtxt")
                salary = jtxt_div.find("u").get_text(strip=True)
                details = jtxt_div.get_text(strip=True).split("|")
                location = details[1].strip()
                experience = details[2].strip()
                education = details[3].strip() if len(details) > 3 else "N/A"

                # 写入CSV
                writer.writerow([company_id, company_name, job_title, hiring_count, job_type, posted_time, salary, location, experience, education])

            print(f"{company_name} 的职位数据已成功写入！")
        else:
            print(f"请求 {company_name} ({company_id}) 的职位数据失败，状态码：{response.status_code}")
