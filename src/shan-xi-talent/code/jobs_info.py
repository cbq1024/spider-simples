import requests
from bs4 import BeautifulSoup
import csv

# 目标 URL
url = "https://sjrc.com.cn/index.php"

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# 发送 HTTP 请求
response = requests.get(url, headers=headers, verify=False)

# 确保响应成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到目标 <ul class="ap_jp_ul"> 标签
    ul_tag = soup.find("ul", class_="ap_jp_ul")

    if ul_tag:
        # 获取所有 <li> 标签
        li_tags = ul_tag.find_all("li")

        # 打开 CSV 文件写入解析内容
        with open("jobs_info.csv", mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)

            # 写入 CSV 文件头
            # csv_writer.writerow(["Company Name", "Job ID"])

            # 遍历 <li> 标签解析内容
            for li in li_tags:
                # 提取公司名称
                company_name_tag = li.find("a", title=True)
                company_name = company_name_tag.text.strip() if company_name_tag else "N/A"

                # 提取“查看全部”链接
                more_details_tag = li.find("div", class_="m").find("a")
                if more_details_tag and "href" in more_details_tag.attrs:
                    more_details_link = more_details_tag["href"]

                    # 提取链接中的 ID 参数值
                    if "id=" in more_details_link:
                        job_id = more_details_link.split("id=")[-1]
                    else:
                        job_id = "N/A"
                else:
                    job_id = "N/A"

                # 写入 CSV 文件
                csv_writer.writerow([company_name, job_id])

        print("数据已成功保存到 jobs_info.csv 文件中！")
    else:
        print("未找到 <ul class='ap_jp_ul'> 标签")
else:
    print(f"请求失败，状态码: {response.status_code}")
