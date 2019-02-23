#coding: utf-8
#!/usr/bin/env python
'''
肖宇晗  1600012821
该部分代码负责根据预处理好的数据建图，迭代计算PageRank值，排序并输出到result.txt文件中
'''
import re
import time
'''
全局变量说明：
class pagePropt：一个页面的属性，包括页面名称，页面的PageRank值，该页面的出度和入度，指向该页面的页面集合（前驱集合）
Pages: 字典，每个item对应一个页面，key为页面的名称（str类型），value为类pagePropt，记录了页面的属性
totalLen: int，记录参与PageRank算法的页面总数量
initPR：float，每个页面初始的PageRank值，程序中会使其等于1/totalLen
selfishPages：字典，每个item对应一个自私的网页（没有出链的网页），key为该网页的名称，
value为其PageRank值除以totalLen（这里是优化，下面会详述）
a: 初始化为0.85，指有85%的人会点击当前页面的链接，15%的人会自己输入一个网址进行跳转
epsilon：初始化为0.00001，当迭代的差值<=epsilon，则结束迭代
PRPages：字典，每个item对应一个网页，key为网页的名称，value为网页的PageRank值，供排序使用
sortedPages: list，存储了排好序的（网页名称，PageRank值）
'''
class pagePropt:
	def __init__ (self):
		self.name = ""
		self.pageRank = 0.0000005
		self.tolen = 0
		self.fromlen =0
		self.fromPages = []
Pages = {}
totalLen = 0
initPR = 0
selfishPages = {}
a = 0.85
epsilon = 0.00001
PRPages = {}
sortedPages = []

'''
读入预处理好的数据（在Pages.txt中），建图
'''
def readin():
	pageFile = open("Pages.txt", "r", encoding='utf-8')
	pageName = re.compile(r'<title>(?P<title>.+)</title>')
	strLine = pageFile.readline()
	while strLine:
		strLine = strLine.strip(" \r\t\n")
		if strLine.startswith("<title>"):
			title = pageName.match(strLine).group('title')
			currPage = pagePropt()
			currPage.name = title
			
			pageFile.readline()  # 把[fromPages]读掉
			strLine = pageFile.readline()
			strLine = strLine.strip(" \t\r\n")
			
			while (strLine == "[toPages]") == False:
				fromPage = strLine
				currPage.fromPages.append(fromPage)
				currPage.fromlen += 1
				strLine = pageFile.readline()
				strLine = strLine.strip(" \t\r\n")
			
			strLine = pageFile.readline()  # 读[toPages]的下面一行
			strLine = strLine.strip(" \r\t\n")
			while strLine.startswith("<title>") == 0:
				if strLine:
					currPage.tolen += 1
					strLine = pageFile.readline()
					strLine = strLine.strip(" \r\t\n")
				else:
					break
		
		Pages[currPage.name] = currPage
	
	pageFile.close()

'''
处理自私的网页（没有出链的网页）,认为它指向所有网页
一开始跑了一遍代码，巨慢无比。最后发现是因为自私网页有50000之多，计算PageRank非常复杂，要把这50000个值全累加一遍。
优化一番之后快了1000多倍，即一开始把所有的自私网页的PageRank都加起来（selfSum），
每个网页在更新PageRank时只要加一次selfSum就可以了，不过对于自私的网页而言，每次更新PageRank之后需要更新一下selfSum
'''
def sefishPages_handler():
	for i in Pages.keys():
		Pages[i].pageRank = initPR
		if Pages[i].tolen == 0:
			selfishPages[i] = Pages[i].pageRank / totalLen  # 在这里就除以totalLen，减少后面的除法
	selfSum = 0
	for i in selfishPages.keys():
		selfSum += selfishPages[i]  # 在这里先加好，由于有50000多个自私网页，在后面一个个加会很耗时，这里加好后面更新即可
		
	return selfSum

'''
将排序好的结果输出到result.txt中
'''
def output():
	resultFile = open("result.txt", "w", encoding="utf-8")
	for i in range(0, totalLen):
		resultFile.write(sortedPages[i][0])
		resultFile.write('\t')
		resultFile.write(str(sortedPages[i][1]))
		resultFile.write('\n')
	resultFile.close()

'''
迭代计算PageRank，如果一次迭代的change(一次迭代中所有页面PageRank变化值的总和)小于epsilon，结束迭代
'''
def PR_algorithm(selfSum):
	prevPR = 0
	change = 10
	iterationTimes = 1
	while change > epsilon:  # 迭代更新pageRank，如果相邻两次迭代之间的差值小于epsilon，迭代结束
		print("iterationTimes: ", iterationTimes)
		iterationTimes += 1
		change = 0
		cnt1 = 0
		cnt2 = 0
		time_1 = time.time()
		for i in Pages.keys():
			prevPR = Pages[i].pageRank
			fromLen = Pages[i].fromlen
			toLen = Pages[i].tolen
			if fromLen > 0:
				fromSum = 0.0
				for j in Pages[i].fromPages:
					toNum = Pages[j].tolen
					if toNum == 0:
						toNum = totalLen
					fromSum += (Pages[j].pageRank / toNum)
				
				fromSum += selfSum
				Pages[i].pageRank = a * fromSum + (1 - a) / totalLen
				if toLen == 0:          # 说明是自私的网页
					selfSum += (Pages[i].pageRank - prevPR) / totalLen  # 对selfSum的值进行更新
				change += abs(prevPR - Pages[i].pageRank)
			else:
				fromSum = 0.0
				fromSum += selfSum
				Pages[i].pageRank = a * fromSum + (1 - a) / totalLen
				change += abs(prevPR - Pages[i].pageRank)
			
			'''
			每更新完10000个页面的PageRank，打印所用时间
			'''
			cnt1 += 1
			if cnt1 >= 10000:
				cnt1 = 0
				cnt2 += 1
				time_2 = time.time() - time_1
				time_1 = time.time()
				print(cnt2, "0000", time_2)
				print("change :", change)


if __name__ == "__main__":
	start = time.time()
	
	readin()    #调用readin()
	
	print("part1 done!")
	time1 = time.time() - start
	print("time1: ", time1)
	
	totalLen = len(Pages.keys())    #设置totalLen
	initPR = 1 / totalLen           #设置initPR
	selfSum = sefishPages_handler() #调用sefishPages_handler()，获得selfSum
	
	print("selfish done!")
	print("selfishPages NUM: ",len(selfishPages.keys()))
	time_selfish = time.time() - start- time1
	print("time_selfish: ", time_selfish)
	
	PR_algorithm(selfSum)           #开始PageRank迭代计算
	
	print("part2 done!")
	time2 = time.time() - start - time1
	print("time2: ", time2)
	
	'''
	下面两个for循环用于排序
	'''
	for i in Pages.keys():
		PRPages[i] = Pages[i].pageRank
	
	sortedPages = sorted(PRPages.items(), key=lambda item: item[1], reverse=True)
	for i in range(0, 1000):
		print(sortedPages[i])
		
	output()                #输出到文件
	
	print("****************")
	print("part3 done!")
	time3 = time.time()- start - time1- time2
	print("time1: ",time1)
	print("time2: ",time2)
	print("time3: ",time3)
	
	