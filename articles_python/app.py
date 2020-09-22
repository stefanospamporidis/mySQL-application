# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import sys, os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import settings


def connection():
    con = db.connect(
    settings.mysql_host, 
    settings.mysql_user, 
    settings.mysql_passwd, 
    settings.mysql_schema)
    
    return con


def classify(topn):
   
    # Create a new connection
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    num=int(topn)
    sql='''select articles.title,articles.summary from articles where articles.id not in (select article_has_class.articles_id from article_has_class)'''
    cur.execute(sql)
    result1=cur.fetchall()
    sql='''select * from classes'''
    cur.execute(sql)
    result2=cur.fetchall()
    list1=[]
    f=[]
    for (i,j) in result1:
        list1=j.split()
        for (x,y,z,w) in result2:
            count=0
            for item in list1:
                if item==z:
                    count+=float(w)
            if count>0:
                f=f+[(i,x,y,count),] #articleId,class,subclass,weight
    out1, out2 = [], []
    for i in f:
        if i[:-1] in out1:
            out2[out1.index(i[:-1])] += i[-1]
        else:
            out1.append(i[:-1])
            out2.append(i[-1])
    out = [tuple(j) + (out2[i],) for i, j in enumerate(out1)]
    Sort(out,3)
    results=[("title","class","subclass","weightsum",),]
    results=results+out
    print(results[:num+1])
    return(results[:num+1])            
#return [("title","class","subclass", "weightsum"),]


def updateweight(class1,subclass,weight):
    
	# Create a new connection
		
    con=connection()
		
	# Create a cursor on the connection
    cur=con.cursor()
    number=int(weight)
    sql='''select class,subclass from classes where weight>%s and class=%s and subclass=%s'''
    cur.execute(sql,(number,class1,subclass))
    count=cur.rowcount
    if (count>0):	
        sql_query='''update classes set weight=weight-((weight-%s)/2) where weight>%s and class=%s and subclass=%s'''
        cur.execute(sql_query,(number,number,class1,subclass))
        con.commit()
        return[("ok")]
    else :
        return[("error")]
    
	
def selectTopNClasses(fromdate, todate,n):

    # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    number=int(n)    
    sql_query='''select a1.class,a1.subclass,count(distinct(articles.id)) as articles_count from articles,article_has_class as a1 where articles.id=a1.articles_id and articles.date between %s and %s group by a1.class,a1.subclass order by articles_count desc limit %s'''
    cur.execute(sql_query,(fromdate,todate,number))
    results=cur.fetchall()
    f=[("class","subclass","count",)]
    results_list = list(results)
    f_results = f + results_list
    print(f_results)
    return f_results


def countArticles(class1,subclass):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    sql_query='''select count(distinct(article_has_class.articles_id)) from article_has_class where article_has_class.class=%s and article_has_class.subclass=%s group by article_has_class.class,article_has_class.subclass'''    
    cur.execute(sql_query,(class1,subclass))
    if (cur.rowcount==1):    
        results=cur.fetchall()
        results_list = list(results)
        f = [("count",)]
        f_results = f + results_list
        print(f_results)
        return f_results    
    else:
        return('0')

# Python code to sort the tuples using float element 
# Inplace way to sort using sort() 
def Sort(tup,i): 
    # reverse = True (Sorts in Descending order) 
    # key is set to sort using float elements 
    # lambda has been used 
    tup.sort(key = lambda x: float(x[i]), reverse = True) 
		
def findSimilarArticles(articleId,n):
    con=connection()
    cur=con.cursor()
    num1=int(articleId)
    num2=int(n)
    sql1='''SELECT articles.summary from articles where articles.id=%s''' #pairnw to articleId pou 8elw gia na sugkrinw to similarity tou me alla articles
    cur.execute(sql1,(num1))
    result1=cur.fetchall()
    sql2='''SELECT articles.id,articles.summary from articles where articles.id!=%s''' #pairnw ta summary olwn twn allwn articles gia na ta sugkrinw me to zitoumeno aricle
    cur.execute(sql2,(num1))
    result2=cur.fetchall()
    for i in result1:
        for j in i:
            list_t = j.split()
            list_tt=[]
            for item in list_t:
                if item not in list_tt:
                    list_tt.append(item)
    #print(list_tt)
    ############## prwti lista ####
    f=[]
    for (i,j) in result2:
        list_v = j.split()
        list_vv=[]
        for item in list_v:
            if item not in list_vv:
                list_vv.append(item)
        #print(list_vv)
        count1=0 #metraei tis koines le3eis tous
        count2=len(list_tt)+len(list_vv)-count1 #metraei tis diaforetikes le3eis kai twn duo 
        for x in list_tt:
            for y in list_vv:
                if x==y:
                    count1+=1
        similarity=count1/count2
        f=f+[(i,similarity,)]
    Sort(f,1)
    results=[("articleId","similarity"),]
    results=results+f
    print(results[:num2+1])
    return(results[:num2+1])