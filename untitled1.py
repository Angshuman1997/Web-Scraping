#Libaries
import os 
import pandas as pd 
import re
from selenium import webdriver as wb
from bs4 import BeautifulSoup
from GrabzIt import GrabzItClient

def name(i):
    try:
        nc=webD.find_element_by_class_name('profile-name') #Finding Company by class name
        return(nc.text)
    except :
        return('Error')
        

def NA(text):
    #Searching for No. of Acquisitions as not all companies have Acquisitions
    p1="Acquisitions"
    if re.search(p1, text):
        a1='YES'
    else:
        a1='NO'
    return(a1)

def NI(text):
    #Searching for No. of Investments as not all companies have Investments
    p2="Investments"
    if re.search(p2, text):
        i1='YES'
    else:
        i1='NO'
    return(i1)
    
def Founder(fn):
    FN=[]
    dt=[]
    for k in range(len(fn)):
        #Find name of founders based on a expression pattern
        p3="person"
        txt = str(fn[k])
        if re.search(p3, txt):
            dt.append(str(fn[k]))
    for k1 in range(len(dt)):
        lg=dt[k1].split('>')
        FN.append(lg[1].strip()[:-3])
    if len(FN)==0:
        FN.append('Not Available in data')
    s=', '.join(FN)
    FN.clear()
    dt.clear()
    return(s)

        
def web():
    #Find appropriate website based on a expression pattern
    w=[]
    w1=[]
    p1='http'
    p2='https'
    if re.search(p1, txt2) or re.search(p2, txt2):
        if re.search(p1+"://www."+comp[i].lower(), txt2) or re.search(p1+"://"+comp[i].lower(), txt2) or re.search(p2+"://www."+comp[i].lower(), txt2) or re.search(p2+"://"+comp[i].lower(), txt2):
            l=txt2.split('/')
            rr=[]
            for j in l:
                if j!='':
                    rr.append(j)
            if len(rr)<=2:
                w=[comp[i],txt2]
                    
        else:
            w1=[comp[i],'No']
    
    
    return(w,w1)
        
def FLT(s):
    #Find appropriate social media account based on a expression pattern
    f=[]
    f1=[]
    if re.search(s, txt2) and (re.search(name(comp[i])[1:], txt2) or re.search(name(comp[i])[1:].lower(), txt2)):
        f=[comp[i],txt2]
    else:
        f1=[comp[i],'No']
        
    return(f,f1)

def reduce(k):
    #Elimnating dublicates
    lm=[list(item) for item in set(tuple(row) for row in k)]
    return(lm)
    

def nan(a):
    #Elimnating None value
    r=[]
    for val in a:
        if val!=[]:
            r.append(val)
    return(r)

def arr(res,res1):
    #Forming required list data
    c=res1.copy()
    if len(res1)>len(res):
        for i in range(len(res1)):
        #print(comp[i])
            for j in range(len(res)):
            #print(lm[j][0])
                if res[j][0]==res1[i][0]:
                    c.remove(res1[i])
    else:
        for i in range(len(res)):
            #print(comp[i])
            for j in range(len(res1)):
                #print(lm[j][0])
                if res1[j][0]==res[i][0]:
                    try:
                        c.remove(res1[j])
                    except:
                        pass
    for i in range(len(c)):
        res.append(c[i])

    return(res)

def arr2(a,b):
    #Rearranging list data
    d=[] 
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i].lower()==b[j][0]:
                d.append(b[j][1])
    return(d)


webD=wb.Chrome(r'C:\Users\Angshuman Bardhan\Desktop\Task1\chromedriver.exe')
comp = list(map(str,input('No. of companies: ').strip().split())) # Multiple Companies can be feed


nam=[]      # List Name
log=[]      # List Path logo
na=[]       # List Acquisitions
ni=[]       # List Investment
ne=[]       # List Employees
founder=[]  # List Founders
fbo=[]      # List Facebook
fbo1=[]     # List Facebook
ldo=[]      # List LinkedIn
ldo1=[]     # List LinkedIn
two=[]      # List Twitter
two1=[]     # List Twitter
wo=[]       # List Website
wo1=[]      # List Website

for i in range(len(comp)):
    source='https://www.crunchbase.com/organization/'+comp[i].lower() #Forming url based on companies
    webD.get(source)
    html = webD.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    #creating folder to store screenshots
    try: 
        path = os.path.join("C:\\Users\\Angshuman Bardhan\\Desktop\\Task1\\", comp[i])
        os.mkdir(path)  
    except :
        pass
    

    
    nAI=soup.find_all('span',class_='component--field-formatter field-type-integer ng-star-inserted')
    
    #NAME OF COMPANY
    nam.append(name(comp[i])) 
    if name(comp[i]) == 'Error':
        print('Invalid company',comp[i]) #Checking if Company name is avaiable or not
        break
    
    #PATH LOGO
    im=soup.find_all('img')
    for r in range(len(im)):
        ss='alt="'+name(comp[i])+' Logo'
        txt1 = str(im[r])
        x=[]
        sd=''
        if re.search(ss, txt1):
            x=txt1.split(' ')
            sd=x[4][5:len(x[4])-1]
    log.append(sd) #PATH LOGO
        
    
    
    #Number of Acquisitions & Investments
    data=[]
    for j in range(len(nAI)):
        lt=str(nAI[j])[77:].strip().split('"')
        data.append(lt[1])
    text = str(html)
    
    if NA(text)=='YES' and NI(text)=='YES':
        na.append(data[0]) #Number of Acquisitions
        ni.append(data[1])#Number of Investments
    
    elif NA(text)=='YES' and NI(text)=='NO':
        na.append(data[0])#Number of Acquisitions
        ni.append('0') #Number of Investments  
    
    elif NA(text)=='NO' and NI(text)=='YES':
        na.append('0') #Number of Acquisitions
        ni.append(data[0]) #Number of Investments 

    else:
        na.append('0') #Number of Acquisitions
        ni.append('0') #Number of Investments
    
    #Number of Employees
    e=soup.find_all('a',class_='component--field-formatter field-type-enum link-accent ng-star-inserted')
    l=str(e[0]).strip().split('>')
    ne.append(l[1][:-3])
    
    #Founders
    fn=soup.find_all('a',class_='link-accent ng-star-inserted')
    founder.append(Founder(fn))
    
    #Links
    grabzIt = GrabzItClient.GrabzItClient("ZDg2NmM1MDVjYTI3NGFkM2FmOTZjMzc4MGE5YTI3MzU=", "bj9UTR8VED8/PxsFUT81PyB4Pz8/d29tSz8UVj8ccU0=")
    for link in soup.find_all('a',href=True):
        lk=link.get('href')
        txt2 = str(lk)
        
        #Website
        wa=web()
        wo.append(wa[0])
        wo1.append(wa[1])
            
        #Facebook
        fa=FLT('facebook')
        fbo.append(fa[0])
        fbo1.append(fa[1])
        
        #LinkedIn
        ld=FLT('linkedin')
        ldo.append(ld[0])
        ldo1.append(ld[1])
               
        #Twitter
        tw=FLT('twitter')
        two.append(tw[0])
        two1.append(tw[1])
        
webs=arr(nan(reduce(wo)),nan(reduce(wo1)))
fbb=arr(nan(reduce(fbo)),nan(reduce(fbo1)))
lid=arr(nan(reduce(ldo)),nan(reduce(ldo1)))
tt=arr(nan(reduce(two)),nan(reduce(two1)))
        
wb=arr2(comp,webs)   #Website
fb=arr2(comp,fbb)  #Facebook
ldd=arr2(comp,lid)#LinkedIn            
twt=arr2(comp,tt) #Twitter

# creating the dataframe 
df = pd.DataFrame({"Name of Company":nam,"Path logo":log,"No. of Acquisitions":na,"No. of Investments":ni,'Founders':founder,'Number of employees':ne,'Website':wb,  'Facebook':fb,'LinkedIn':ldd,'Twitter':twt}) 
df 

#HTML Table
htmll = df.to_html() 
text_file = open("Company Table.html", "w") 
text_file.write(htmll) 
text_file.close() 

#Forming CSV File
df.to_csv (r'Company Table.csv', index = False, header=True)

#Screenshot
for x1 in range(len(comp)):
    for y1 in range(len(webs)):
        
        #Website
        if comp[x1].lower()==webs[y1][0]:
            if webs[y1][1]!="No":
                grabzIt.URLToImage(webs[y1][1])
                filepath = r"C:\\Users\\Angshuman Bardhan\\Desktop\\Task1\\"+comp[x1]+"\\website.jpg"
                grabzIt.SaveTo(filepath)
        
        #Facebook        
        if comp[x1].lower()==fbb[y1][0]:
            if fbb[y1][1]!="No":
                grabzIt.URLToImage(fbb[y1][1])
                filepath = r"C:\\Users\\Angshuman Bardhan\\Desktop\\Task1\\"+comp[x1]+"\\facebook.jpg"
                grabzIt.SaveTo(filepath)
                
        #LinkedIn       
        if comp[x1].lower()==lid[y1][0]:
            if lid[y1][1]!="No":
                grabzIt.URLToImage(lid[y1][1])
                filepath = r"C:\\Users\\Angshuman Bardhan\\Desktop\\Task1\\"+comp[x1]+"\\linkedin.jpg"
                grabzIt.SaveTo(filepath)
                
        #Twitter
        if comp[x1].lower()==tt[y1][0]:
            if tt[y1][1]!="No":
                grabzIt.URLToImage(tt[y1][1])
                filepath = r"C:\\Users\\Angshuman Bardhan\\Desktop\\Task1\\"+comp[x1]+"\\twitter.jpg"
                grabzIt.SaveTo(filepath)

    
webD.close()
    


    