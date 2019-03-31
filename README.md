## Web Data Mining—PageRank Algorithm
**Yuhan Xiao**  

------

[TOC]

------

------

### 1. 数据源  
- 名称：enwiki-20180920-pages-articles-multistream  

- 文件类型：xml文件  

- 总大小：64.2GB  

- 分析提取的页面数量：2,000,000  

- 过滤后并在PageRank中使用到的页面数量：1,138,447  

------

### 2. PageRank算法公式  
![image](https://wx4.sinaimg.cn/large/0071tMo1ly1fwg8wna931j307n022jrw.jpg)  

------

### 3. 代码概述  
#### 3.1 processData.py  
##### 3.1.1 目的与作用  
- 从xml文件中读入并处理页面数据  
- 将预处理好的数据输出到Pages.txt和effPages.txt中
	- Pages.txt中为预处理好的页面数据  
	- effPages.txt仅为调试所用，可忽略  
- Pages.txt数据格式如下：
```
<title>fromPages]</title>  
[fromPages]
A  
B  
……  
[toPages]  
A  
B  
……  
```
![image](https://wx3.sinaimg.cn/large/0071tMo1ly1fwg6e9ucx6j30a10b0dg1.jpg)  

##### 3.1.2 全局变量说明  
- class pagePropt：  
	一个页面的属性，包括页面名称，该页面指向的页面的集合（后继集合），指向该页面的页面集合（前驱集合）  
	![image](https://wx3.sinaimg.cn/large/0071tMo1ly1fwg6g6qhw5j307502ydg1.jpg)  
- Pages：
	字典，每个item对应一个页面，key为页面的名称（str类型），value为类pagePropt，记录了页面的属性  
- Links：  
	集合，记录了2000,000页面所出现的所有链接，为后面做集合运算用。由于是集合，所以无重复元素  

##### 3.1.3 main函数说明  
###### part1  
第43--97行为读取xml文件，共读取2000,000个页面，解析出[[ ]]内的内容，进行过滤操作删掉不需要的词条后存入字典Pages和集合Links中  
- 第59--65行提取页面标题（```<title>页面标题</title>```）  
- 第70--87行提取[[ ]] 内的内容，对于形式为[[ A | B ]]的，用B就好；形式为[[AAA | BBB | CCC]]的，用A就好  
- 第91--97行负责打印每处理完1000个页面所用的时间  
###### part2  
- 第107--109行：取2000,000个页面与它们的所有链接的交集，作为effPages（set类型）  
- 第114--117行：去掉每个页面不在effPages中的后继  
- 第122--126行：根据每个页面的toPages添加在effPages中的前驱  
###### part3  
文件写入，将预处理好的数据输出到Pages.txt和effPages.txt中。前面已经阐释了，这里不在赘述  
##### 3.1.4 优化说明
- 主要就是使用了set数据结构而非list  
	- 对每个页面而言，出链和入链都是用set存的，既去重，又快捷，再加节省内存  
	- 在part2取交集时，用set最为快捷省时  


#### 3.2 compute.py  

##### 3.2.1 目的与作用  
- 根据预处理好的数据建图  
- 迭代计算PageRank值  
- 排序并输出到result.txt文件中  
##### 3.2.2 全局变量说明  
- class pagePropt：  
	一个页面的属性，包括页面名称，页面的PageRank值，该页面的出度和入度，指向该页面的页面集合（前驱集合）  
- Pages:  
	字典，每个item对应一个页面，key为页面的名称（str类型），value为类pagePropt，记录了页面的属性  
- totalLen:  
	int，记录参与PageRank算法的页面总数量  
- initPR：  
	float，每个页面初始的PageRank值，程序中会使其等于1/totalLen  
- selfishPages：  
	字典，每个item对应一个自私的网页（没有出链的网页），key为该网页的名称，value为其PageRank值除以totalLen（这里是优化，下面会详述）  
- a:  
	初始化为0.85，指有85%的人会点击当前页面的链接，15%的人会自己输入一个网址进行跳转  
- epsilon：  
	初始化为0.00001，当迭代的差值<=epsilon，则结束迭代  
- PRPages：  
	字典，每个item对应一个网页，key为网页的名称，value为网页的PageRank值，供排序使用  
- sortedPages:  
	list，存储了排好序的（网页名称，PageRank值）  
##### 3.3.3 函数说明  
- def readin()  
	读入预处理好的数据（在Pages.txt中），建图  
- def sefishPages_handler()  
	处理自私的网页（没有出链的网页）,认为它指向所有网页  
一开始跑了一遍代码，巨慢无比。最后发现是因为自私网页有50000之多，计算PageRank非常复杂，要把这50000个值全累加一遍。优化一番之后快了1000多倍，即一开始把所有的自私网页的PageRank都加起来（selfSum），每个网页在更新PageRank时只要加一次selfSum就可以了，不过对于自私的网页而言，每次更新PageRank之后需要更新一下selfSum  

- def output()  
	将排序好的结果输出到result.txt中  
- def PR_algorithm(selfSum)  
	迭代计算PageRank，如果一次迭代的change(一次迭代中所有页面PageRank变化值的总和)小于epsilon，结束迭代  
- 排序部分：第183--188行。对PageRank进行排序，结果放到sortedPages中  



------


### 4.  PageRank值分析  
- 共迭代了25次  
- 前20名中，国家和地区占多数(TW是台湾的简写)  
	![image](https://wx2.sinaimg.cn/large/0071tMo1ly1fwg82bq190j30d00cvjrw.jpg)  
- 前30名PageRank值差异较大，后面的差异较小  

------

### 5. 碰到的问题与相应解决方案  
- 首先是processData.py中，如何提取词条而不会内存爆炸或者过于缓慢  
`这方面的解决方法主要是通过把list数据类型改为set类型，自动去重，操作省时，节省内存`  
- compute.py中，内存爆炸问题  
`把每个页面的toPages属性去掉，改为tolen（int型），反正已经有了fromPages了，不需要toPages
`
`一开始把所有自私网页的所有属性都另存下来，最后发现有用的只有它们的PageRank，所以只另存了PageRank`
- compute.py中，PageRank算法过慢的问题  
  `最后发现主要是自私网页导致的问题，数据中自私网页很多，50000多个。每次更新会非常慢，起码每个网页需要执行50000多次加法。因此，在selfishPages.handler函数中，预先累加所有自私网页的PageRank到selfSum，这样对每个网页来讲，每次更新只需要加上一个selfSum，而不是执行50000多次加法。不过对于自私的网页而言，每次更新PageRank之后需要更新一下selfSum。经过以上优化，速度快了1000多倍 `  

  `此外，为了尽可能减少运行时间，很多循环内的除法都在循环之外预先算好`
  `经过以上优化，运行一次compute.py的时间为10分钟左右`
