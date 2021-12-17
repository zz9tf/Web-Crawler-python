import requests, re, csv, os.path
import datetime
import time


def dateTf(date):
    '''
    This method transfer a string date like "2021-12-16" to an int "20211216"
    :param date: A string with the style "year-month-date"
    :return: An int with the style "YearMonthDate"
    '''
    date = date.split("-")
    return sum([int(date[0]) * 10000 + int(date[1]) * 100 + int(date[2])])


def writeDataInCSV(date):
    '''
    This method will write the date's data in a CVS file
    :param date: A string represents the date of today.
    :return: None
    '''
    csvfile = open(str(datetime.date.today()) + ".csv", "w", newline="", encoding="gbk")
    writer = csv.writer(csvfile)
    writer.writerow(["代码", "名称", "价格", "涨跌幅", "涨跌额", \
                     "5分钟涨", "今开", "昨收", "最高", "最低", \
                     "成交量", "成交额", "换手率", "量比", "委比", \
                     "振幅", "市盈率", "流通市值", "总市值", "每股收益",
                     "净利润", "主营收"])
    for i in range(184):
        print(str(i + 1) + "/184")
        url = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=" + \
              str(i) + \
              "&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query"
        getData(url, writer)
    csvfile.close()


def getData(url, writer):
    print("Data Downloading...")
    # 获取网站原信息
    while (True):
        try:
            response = requests.get(url, timeout=5)
            break
        except:
            print("Reloading...")
    oriData = response.text
    oriData = re.sub("\"", "", oriData)

    # 解析网站信息
    datalists = re.findall("(CODE.*?NO:\d+)\}", oriData, re.S)
    Dics = []
    for list in datalists:
        list = list.split(",")
        stockDic = {}
        for item in list:
            item = item.split(":")
            if len(item) == 3:
                item = item[1:]
            if item[0] == "CODE":
                stockDic["代码"] = item[1]
            elif item[0] == "NAME":
                stockDic["名称"] = item[1].encode("utf-8").decode("unicode_escape")
            elif item[0] == "PRICE":
                stockDic["价格"] = item[1]
            elif item[0] == "PERCENT":
                stockDic["涨跌幅"] = item[1]
            elif item[0] == "UPDOWN":
                stockDic["涨跌额"] = item[1]
            elif item[0] == "FIVE_MINUTE":
                stockDic["5分钟涨"] = item[1]
            elif item[0] == "OPEN":
                stockDic["今开"] = item[1]
            elif item[0] == "YESTCLOSE":
                stockDic["昨收"] = item[1]
            elif item[0] == "HIGH":
                stockDic["最高"] = item[1]
            elif item[0] == "LOW":
                stockDic["最低"] = item[1]
            elif item[0] == "VOLUME":
                stockDic["成交量"] = item[1][:-2] + '.' + item[1][-2:]
            elif item[0] == "TURNOVER":
                stockDic["成交额"] = item[1]
            elif item[0] == "HS":
                stockDic["换手率"] = item[1]
            elif item[0] == "LB":
                stockDic["量比"] = item[1]
            elif item[0] == "WB":
                stockDic["委比"] = item[1]
            elif item[0] == "ZF":
                stockDic["振幅"] = item[1]
            elif item[0] == "PE":
                stockDic["市盈率"] = item[1]
            elif item[0] == "MCAP":
                stockDic["流通市值"] = item[1]
            elif item[0] == "TCAP":
                stockDic["总市值"] = item[1]
            elif item[0] == "MFSUM":
                stockDic["每股收益"] = item[1]
            elif item[0] == "{MFRATIO2":
                stockDic["净利润"] = item[1]
            elif item[0] == "MFRATIO10":
                stockDic["主营收"] = item[1][:-1]
        Dics.append(stockDic)
    # csv存储
    seq = ["代码", "名称", "价格", "涨跌幅", "涨跌额", \
           "5分钟涨", "今开", "昨收", "最高", "最低", \
           "成交量", "成交额", "换手率", "量比", "委比", \
           "振幅", "市盈率", "流通市值", "总市值", "每股收益",
           "净利润", "主营收"]
    for dic in Dics:
        rowvalue = []
        for key in seq:
            try:
                rowvalue.append(dic[key])
            except:
                print("Not found:" + dic["名称"] + ": " + key)
                rowvalue.append("")
        writer.writerow(rowvalue)
    print("Data has been download!\n")

def uploadDate(date):
    '''
    This method will split the data got from today, and put them into
    different stock CSV files.
    :param date: A string represents the date of today.
    :return: None
    '''
    print("Date updating...")
    with open(date + ".csv", "r", encoding="gbk") as dailyData:
        CONTENTS = dailyData.readlines()
        head = CONTENTS[0].strip("'\n").split(",")
        head.insert(0, "日期")

        for line in CONTENTS[1:]:
            line = line.strip("'\n").split(",")
            line.insert(0, date)
            path = "stocks/" + line[1] + ".csv"
            if not os.path.isdir("./stocks"):
                os.mkdir("./stocks")

            if not os.path.isfile(path):
                # 没在数据库中找到目标股票或目标股票数据丢失
                stock = open(path, "w", newline="", encoding="gbk")
                writer = csv.writer(stock)
                writer.writerow(head)
                print(head)
                writer.writerow(line)
                print(line)
            else:
                # 在数据库中找到了目标股票
                with open(path, "r", encoding="gbk") as stock:
                    stock_lines = stock.readlines()
                stock = open(path, "w", newline="", encoding="gbk")
                writer = csv.writer(stock)
                print(line)
                # 更新信息
                for row_id in range(len(stock_lines)):
                    stock_lines[row_id] = stock_lines[row_id].strip("\n").split(",")
                    if stock_lines[row_id][0] == date:
                        stock_lines[row_id] = line.copy()
                        print("Renew: " + str(line))
                        line.insert(0, -1)
                if line[0] != -1:
                    stock_lines.append(line)
                # 写入程序
                writer.writerow(stock_lines[0])
                for stock_line in sorted(stock_lines[1:], key=lambda x: dateTf(x[0])):
                    writer.writerow(stock_line)
            stock.close()
    print("Data has been updated")


def isWorkday(date):
    '''
    This method will return a boolean about if the date is a workday.
    :param date: A sting represents the date with the style "year-mon-day"
    :return: A boolean represents if today is a workday
    '''
    # 下载数据
    url = r"https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?tn=wisetpl&format=json&resource_id=39043&query=" \
          + date[0:4] \
          + r"%E5%B9%B4" \
          + str(int(date[5:6])) \
          + r"%E6%9C%88&t=1639708282692&cb=op_aladdin_callback1639708282692"
    response = requests.get(url)
    contents = response.text.split('"oDate":')
    date = datetime.datetime.strptime(date[2:], '%y-%m-%d')
    date = str(date.replace(year=date.year - 1, day=date.day - 1))
    normalWorkday = ["一", "二", "三", "四", "五"]

    # 解析数据，确认是周一到周五且不是节假日
    for index in range(len(contents)):
        if date[:10] in contents[index]:
            if contents[index][203:204] in normalWorkday:
                if "status" not in contents[index]\
                        or ("status" not in contents[index] and contents[index][37:38] != '1'):
                    return True
    return False

def recordUpdateDate(date):
    '''
    This method records the date and the time that you download the stock data.
    :param date: A string represents the date of today
    :return: None
    '''
    updateRecorder = open("updateRecord.txt", "a+")
    updateRecorder.write(date + " " + time.strftime("%H:%M:%S", time.localtime()) + "\n")
    updateRecorder.close()
    print("Today has been recorded")

def main():
    date = str(datetime.date.today())
    print("Today is " + date + ".")
    # 确定是工作日
    if isWorkday(date):
        print("Today is a workday.")

        # 确定到达爬取时间
        print("waiting...")
        while time.strftime("%H:%M:%S", time.localtime()) != "20:00:00":
            continue
        print("\nNow is " + time.strftime("%H:%M:%S", time.localtime()) + "\nTime to get data:")

        # 爬取数据
        writeDataInCSV(date)

        # 将今天的数据更新进数据库
        uploadDate(date)

        # 记录数据更新日期
        recordUpdateDate(date)

    else:
        print("Today is not a workday.")
    # 程序进入休眠状态
    time.sleep(60 * 60 * 11 + 60 * 50)  # 60sec*60min*11H + 60*50 （11H 50 min)留一些空隙时间防止程序出问题
    print("Ready for the next day!")


main()
