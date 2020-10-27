from django.shortcuts import render
from django.contrib.auth.models import User #导入模块，创建用户
from django.contrib.auth import authenticate  #导入模块，验证用户
from django.shortcuts import redirect   #导入重定向模块
from django.contrib.auth.decorators import login_required   #判断无session，返回首页
from django.contrib.auth import login,logout  #存session用、注销清理session用
from .models import *  #导入models模块
from django.http import HttpResponse  #导入响应模块
import random  #用于随机生成密码
from django.core.mail import send_mail  #发送邮件用的
from pwSave import settings  #导入settings
import datetime  #导入时间模块
from .PwEDE import * #导入加密解密模块
from .models import *  #导入数据表
from django.core.paginator import Paginator #导入分页模块



def check_in_blacklist(user):  #检测用户是否在黑名单中
	return not user.username in settings.LOGIN_BLACKLIST



def tt(request):
    # print(test1)
    return render(request,'appPw/test.html',)



#注册页面
def register(request):
    if request.method=='POST':
        uid=request.POST['username']
        pwd=request.POST['pwd']
        re_pwd=request.POST['re_pwd']
        email1=request.POST['email']
        if not uid or not pwd or not email1: #判断用户名是否存在
            con={'username':uid,'info':'参数不能设置为空！！！','email':email1}            
            return render(request,'appPw/register.html',con)
        elif  User.objects.filter(username=uid):
            con={'username':uid,'info':'用户名已经存在！！！','email':email1}            
            return render(request,'appPw/register.html',con) 
        elif User.objects.filter(email=email1):
            con={'username':uid,'info':'邮箱已存在！！！','email':email1}
            return render(request,'appPw/register.html',con)
         
        elif pwd!=re_pwd:  #判断两次输入的密码是否一致
            con={'username':uid,'info':'输入的两次密码不一致！！！','email':email1}
            return render(request,'appPw/register.html',con)
        else :
            User.objects.create_user(uid,email1,pwd) #用于创建普通用户
            # userID=User.objects.filter(username='admin3').values()[0]['id']  #获取到用户id
            # UserInfo(userId=userID,name=name).save()  #保存id和姓名到userinfo表里面
            con={'info':'注册成功！请登录！'}
            return render(request,'appPw/register.html',con)
    else:
        return render(request,'appPw/register.html')

#登录页面
def loginn(request):
    uid=''
    news=''
    if request.method=='POST':
        uid=request.POST['name']
        pwd=request.POST['pwd']
        user=authenticate(username=uid,password=pwd)  #验证用户名密码
        if user is not None:
            login(request,user) #执行登录操作，存session
            #设置存session过期时间60秒 0代表退出浏览器就过期 None则意思是session永不清除。 不设置半个月过期
            request.session.set_expiry(0) 
            request.session.clear_expired()  #清理已过期session
            return redirect('main') #重定向到       main 这个值是url后面name那个那么值
        else:
            news='用户名密码错误！'
        context={'name':uid,'news':news}
        return render(request,'appPw/loginn.html',context)
    elif request.user.is_authenticated:  #判断有没有session，有返回ture执行下面的
        return redirect('main')  #如果登录了 就重定向到name=loginok的url上面
    elif request.method=='GET': 
        return render(request,'appPw/loginn.html')
#注销
def quit(request):
    #清理session
    logout(request)
    return redirect('loginn') 


#随机生成10位数密码
def genPw():
    ss= "abcdefghiFGHIJKTUVWXYZ123456789LMNOPQRS0!@#$%^&jklmnopqrstuvwxyzABCDE*"
    pw=''
    for i in range(0,10):
        n=random.randint(0,69)
        p=ss[n]
        pw+=p
    return pw


#找回密码页面
def findpw(request):
    if request.method=='POST':
        email1=request.POST['email']
        if User.objects.filter(email=email1) and email1: #如果存在就改密码发送到邮箱
            sjpw=genPw()  #随机生成密码
            user=User.objects.get(email=email1)  #获取用户名
            user.set_password(sjpw)  #修改密码
            user.save()

            msg = '用户名：'+str(user)+'\n密码：'+sjpw
            send_mail(
                subject='密码已重置！！！',
                message=msg,
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=[email1]               # 这里注意替换成自己的目的邮箱

            )
            con={'info':'密码已重置，请登录邮箱查看'}
            return render(request,'appPw/findpw.html',con)
        else:
            con={'info':'无此邮箱！！！','email':email1}
            return render(request,'appPw/findpw.html',con)            

    return render(request,'appPw/findpw.html')


#修改密码
def changePw(request):
    if request.method=='POST':
        oldpwd=request.POST['oldpwd']
        newpwd=request.POST['newpwd']
        newpwd2=request.POST['newpwd2']
        user=request.user #获取用户名

        if not oldpwd or not newpwd or not newpwd2:
            con={'info':'参数不能空！！！'}
            return render(request,'appPw/changePw.html',con)
        if newpwd!=newpwd2:
            con={'info':'两次密码不一样！！！'}
            return render(request,'appPw/changePw.html',con)
        if user.check_password(oldpwd):  #验证老密码是否一样
            user.set_password(newpwd)  #修改密码
            user.save()
            con={'info':'密码修改成功，请记住！！！'}
            return render(request,'appPw/changePw.html',con)
        else:
            con={'info':'旧密码不对！！'}
            return render(request,'appPw/changePw.html',con)


    return render(request,'appPw/changePw.html')

    #登录主页
@login_required
def main(request):
    username=request.user #获取到登录的用户名
    con={'username':username}
    return render(request,'appPw/main.html',con)

#添加信息
@login_required
def pwadd(request):
    if request.method=='POST':
        webname=request.POST['webname'] #网站名
        weblink=request.POST['weblink']  #网址
        username=request.POST['username']  #用户名
        password=request.POST['password']  #密码
        pwSK=request.POST['pwSK']  #6位数秘钥
        pwd=encrypted(password,pwSK) #传入密码和秘钥加密，得到加密的密码
        other=request.POST['other']  #备注
        nowtime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间
        userID=request.user.id  #获取到表auth_user里用户的对应的id
        if pwInfo.objects.filter(webname=webname,userID=userID):
            con={'info':'提示：网站名已存在','webname':webname,'weblink':weblink,'username':username,'pwSK':pwSK,'other':other,'password':password}
            return render(request,'appPw/pwadd.html',con)
        pwInfo(webname=webname,weblink=weblink,username=username,password=pwd,time=nowtime,other=other,userID=userID).save()
        pwInfoLog(webname=webname,time=nowtime,userID=userID,changelog='添加信息').save()
        return redirect('pwShow',pageid=1,page=15)
    return render(request,'appPw/pwadd.html',)

#信息列表
@login_required
def pwShow(request,pageid,page):

    userID=request.user.id  #获取到表auth_user里用户的对应的id
    people_list=pwInfo.objects.filter(userID=userID).order_by("-time")   #获取所有数据已时间倒序排列
    paginator=Paginator(people_list,page)     ##创建一个paginator对象,每页拿10个
    page1=paginator.page(pageid)   ##每次拿一页,传入第几页
    con={'pagelist':page1,'page':page}
    return render(request,'appPw/pwShow.html',con)

#删除信息
@login_required
def deletePw(request,webname,time):
    userID=request.user.id  #获取到表auth_user里用户的对应的id
    pwInfo.objects.filter(webname=webname,time=time,userID=userID).delete()
    nowtime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间
    pwInfoLog(webname=webname,time=nowtime,userID=userID,changelog='删除信息').save()
    return redirect('pwShow',pageid=1,page=15)

#解密密码
@login_required
def decryption(request,userID,webname):
    if request.method=='POST':
        nowtime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间
        pw=pwInfo.objects.filter(userID=userID,webname=webname)[0].password
        print(pw)
        decryption=request.POST['decryption']
        p=decrypted(pw,decryption) #解密
        if p=='解密失败':
            con={'info':p}
            pwInfoLog(webname=webname,time=nowtime,userID=userID,changelog='解密失败').save()
        else:
            con={'info':'密码是：'+p}
            pwInfoLog(webname=webname,time=nowtime,userID=userID,changelog='解密成功').save()
        return render(request,'appPw/decryption.html',con)

    return render(request,'appPw/decryption.html')

#信息列表里面的修改密码
@login_required
def infoChangePw(request,userID,webname,username):
    if request.method=='POST':
        pw1=request.POST['newPw1']  #密码
        pw2=request.POST['newPw2']  #密码
        decryption=request.POST['decryption']  #密码
        if pw1==pw2:            
            pwd=encrypted(pw1,decryption) #传入密码和秘钥加密，得到加密的密码
            nowtime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间

            pwInfo.objects.filter(userID=userID,webname=webname,username=username).update(password=pwd,time=nowtime)
            pwInfoLog(webname=webname,time=nowtime,userID=userID,changelog='修改密码').save()

            con={'webname':webname,'info':'密码修改成功','newPw1':pw1,'newPw2':pw2,'decryption':decryption}
            return render(request,'appPw/infoChangePw.html',con)

        else:
            con={'webname':webname,'info':'两次密码不一致','newPw1':pw1,'newPw2':pw2,'decryption':decryption}
            return render(request,'appPw/infoChangePw.html',con)            

    con={'webname':webname}

    return render(request,'appPw/infoChangePw.html',con)

#操作日志
@login_required
def logShow(request,pageid,page):
    userID=request.user.id  #获取到表auth_user里用户的对应的id
    people_list=pwInfoLog.objects.filter(userID=userID).order_by("-time")   #获取所有数据已时间倒序排列
    paginator=Paginator(people_list,page)     ##创建一个paginator对象,每页拿10个
    page1=paginator.page(pageid)   ##每次拿一页,传入第几页
    con={'pagelist':page1,'page':page}
    return render(request,'appPw/logShow.html',con)