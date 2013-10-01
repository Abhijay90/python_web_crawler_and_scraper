from bs4 import BeautifulSoup
import urllib2
import urlparse
from lxml import etree as et
import re
count=0
key=[]
final_list={}
fo=open('','r')# file address for keywords file
fs=open('','r')#file address for list of website  file
fw=open('','w')#file address for output file
for k in fo:
    key.append(re.compile(k.strip('\n')))
def spider():
    global fs,count
    web=[]
    c=0
    for url in fs:
        url=url.strip('\n')
        web.append(url)
    urls=set()
    url_visited=set()
    while(True):
        try:
            url=urls.pop()
        except:
             try:
                 url=web[c]
                 if(c==10):
                     raise Exception
                 c+=1
                 url_head=urlparse.urlparse(url).hostname
             except:
                 print('process over exiting')
                 return 

        try:
            html=urllib2.urlopen(url).read()
            print url
            #if (count==1):
             #   return
            d=0
        except:
            d=1
        if(d==0):
            soup=BeautifulSoup(html)
            scrap(html,url)
            for tag in soup.findAll('a',href=True):
                addr2=urlparse.urlparse(tag['href']).path
                addr1=urlparse.urlparse(tag['href']).hostname
                if(addr1==None):
                    addr=url+addr2
                else:
                    if(url_head in addr1):
                        addr=addr1+addr2
                if(not((addr in url) or (addr in url_visited))):
                    #urls.add(addr)
                    pass
        url_visited.add(url)
        #print len(urls)
        
def display(keyword,path,url,span,string):
    #print "url: ",url
    #print "keyword:",keyword
    #print "path:", path
    global count
    for r in span:
        start=r[0]
        end=r[1]
        new_string=""
        print "hello"
        for i in range(len(string)):
            new_string=new_string+string[i]
            if (i==start-1):
                new_string=new_string+"<mark>"
            if(i==end-1):
                new_string=new_string+"</mark>"
        string=new_string
    global final_list
    final_list[keyword]=[url,path,string]
    print len(final_list)
    #if(len(final_list)>5):
     #   count=1
def scrap(html,url):
    global key
    d=[]
    root = et.HTML(html)
    tree = et.ElementTree(root)
    for e in tree.iter():
        d.append(tree.getpath(e))
    for e in d:
        element=root.xpath(str(e))
        s=element[0].text
        #print s
        if(s!= None ):
            for pattern in key:
                k=[]
                c=1
                for match in re.finditer(pattern,string=s):
                    k.append(match.span())
                    c=0
                if(c==0):
                    path=e
                    keyword=pattern.pattern
                    span=k
                    string=s
                    display(keyword,path,url,span,string)
def main():
    spider()
    global fs,fo,final_list,fw
    fw.write('<html xmlns="http://www.w3.org/1999/xhtml">\
    <head>\
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
    <title>Untitled Document</title>\
    </head>\
    <body>\
    <table width="200" border="1">')
    for element in final_list:
        print element
        fw.write("<tr id="+element+">\n")
        fw.write("<td id=1>"+element+"</td>\n")
        fw.write("<td id=2>"+final_list[element][0]+"</td>\n")
        fw.write("<td id=3>"+final_list[element][1]+"</td>\n")
        fw.write("<td id=4>"+final_list[element][2].encode("UTF-8")+"</td>\n")
        fw.write("</tr>\n")
    fw.write('</body>\
    </html>')
    fo.close()
    fs.close()
    fw.close()
    
    #print final_list

main()
