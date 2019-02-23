#coding: utf-8
#!/usr/bin/env python
'''
肖宇晗  1600012821
该部分代码用于读入并处理页面数据，将预处理好的数据输出到Pages.txt和effPages.txt中，effPages.txt仅为调试所用，可忽略
Pages.txt为预处理好的数据
Pages.txt数据格式：
<title>页面标题</title>
[fromPages]
A
B
……
[toPages]
A
B
……
'''
import re
import time
'''
全局变量说明：
class pagePropt：一个页面的属性，包括页面名称，该页面指向的页面的集合（后继集合），指向该页面的页面集合（前驱集合）
Pages: 字典，每个item对应一个页面，key为页面的名称（str类型），value为类pagePropt，记录了页面的属性
Links：集合，记录了2000,000页面所出现的所有链接，为后面做集合运算用。由于是集合，所以无重复元素
'''
class pagePropt:
	def __init__ (self):
		self.name = ""
		self.toPages = set()
		self.frompages = set()
Pages = {}
Links = set()

'''
main函数
由于操作不多，所以没有分函数写
'''
if __name__ == '__main__':
	
	start = time.time()
	'''
	下面第43--97行为读取xml文件，解析出[[ ]]内的内容，进行过滤操作删掉不需要的词条后存入字典Pages和集合Links中
	'''
	rawdata_path = "E:\enwiki-20180920-pages-articles-multistream.xml"
	pageName = re.compile(r'<title>(?P<title>.+)</title>')
	ref_regex = re.compile(r'\[\[([^\[\]]+)\]\]')
	xmlFile = open("E:\enwiki-20180920-pages-articles-multistream.xml","r",encoding = "utf-8")
	for i in range(0,44):
		strLine = xmlFile.readline()
	cnt1 = 0
	cnt2 = 0
	time_1 = time.time()    #为打印运行时间而设
	for i in range(0,100000):
		strLine = xmlFile.readline()
		strLine = strLine.strip(' \t\r\n')
	
		'''
		提取页面标题
		'''
		if strLine == "<page>":
			strLine = xmlFile.readline()
			strLine = strLine.strip(' \t\r\n')
			if strLine.startswith('<title>'):
				title = pageName.match(strLine).group('title')
				currPage = pagePropt()
				currPage.name = title
			
			'''
			提取[[ ]] 内的内容，对于形式为[[ A | B ]]的，用B就好；形式为[[AAA | BBB | CCC]]的，用A就好
			'''
			while(len(re.findall(r'</page>',strLine)) == 0):
				strLine = xmlFile.readline()
				refs = []
				for ref in ref_regex.findall(strLine):
					if ref.startswith(('Wikipedia:', 'Category:', ':Category:','1','2')):
						continue
					refs = list(ref.split('|'))
					if len(refs) == 3:
						content = refs[0]
					elif len(refs) == 2:
						content = refs[1]
					else:
						content = refs[0]
						
					currPage.toPages.add(content)
					Links.add(content)
					
			Pages[currPage.name] = currPage
			'''
			每处理完1000个页面打印所用时间
			'''
			cnt1 += 1
			if cnt1 >= 1000:
				cnt2 += 1
				cnt1 = 0
				time_2 = time.time() - time_1
				time_1 = time.time()
				print(cnt2,"000",time_2)
				
	print("part1 done!")
	end1= time.time()
	time1= end1-start
	print("time1: ", time1)
	
	'''
	取2000,000个页面与它们的所有链接的交集，作为effPages（set类型）
	'''
	Pages_set = set(Pages.keys())
	effPages = Links & Pages_set  #有效的page
	effPages_len = len(effPages)
	
	'''
	去掉每个页面不在effPages中的后继
	'''
	for i in Pages.keys():
		if i not in effPages:
			continue
		Pages[i].toPages = Pages[i].toPages & effPages
	
	'''
	根据每个页面的toPages添加在effPages中的前驱
	'''
	for i in Pages.keys():
		if i not in effPages:
			continue
		for j in Pages[i].toPages:
			Pages[j].frompages.add(i)
	
	print("part2 done!")
	time2 = time.time() - start- time1
	print("time2: ", time2)
	
	'''
	文件写入
	'''
	pagesFile = open("Pages.txt","w", encoding = 'utf-8')
	for i in effPages:
		pagesFile.write("<title>"+i+"</title>\n")
		pagesFile.write("[fromPages]\n")
		for j in Pages[i].frompages:
			pagesFile.write(j+"\n")
		pagesFile.write("[toPages]\n")
		for j in Pages[i].toPages:
			pagesFile.write(j+"\n")
	effPagesFile = open("effPagesFile.txt","w",encoding = "utf-8")
	for i in effPages:
		effPagesFile.write(i+'\n')
	time3 =time.time() - start - time1- time2
	print("time3: ", time3)
	
	
	xmlFile.close()
	pagesFile.close()
	effPagesFile.close()
	print("time1: ",time1)
	print("time2: ",time2)
	print("time3: ",time3)
	print("effPages number: ", effPages_len)