from django.urls import path  #导入url解析函数
from django.urls import re_path  #导入正则函数
from . import views  #导入视图
from django.contrib.admin.utils import quote
urlpatterns=[

	path('tt/',views.tt,),


	path('register/',views.register,name='register'),  #注册页面
	path('',views.loginn,name='loginn'),  #登录首页
	path('main/',views.main,name='main'),  #登录成功的首页
	path('quit/',views.quit,name='quit'),  #退出登录，清理session


	path('findpw/',views.findpw,name='findpw'),  #找回密码
	path('changePw/',views.changePw,name='changePw'),  #修改密码
	path('pwadd/',views.pwadd,name='pwadd'),   #添加信息
	path('pwShow/<pageid>/<page>',views.pwShow,name='pwShow'),   #信息列表
	path('deletePw/<webname>/<time>/',views.deletePw,name='deletePw'),  #删除信息

	path('infoChangePw/<userID>/<webname>/<username>/',views.infoChangePw,name='infoChangePw'),  #信息列表里面的修改密码
	path('decryption/<userID>/<webname>/',views.decryption,name='decryption'),  #解密
	
	path('logShow/<pageid>/<page>',views.logShow,name='logShow'),   #操作日志

	]