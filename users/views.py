from django.shortcuts import render,redirect
from .models import User,SetCookie123
import os
import time

# Create your views here.
def user_detail_view(request,*args,**kwargs):
	if request.method=="GET":
		if return_username_from_cookie(request) ==None:
			return redirect('/')
		else:
			username_obtained=return_username_from_cookie(request)
			return render(request,"dropbox3.html",{"my_username":username_obtained,"var":'user'})
	try:
		obj=User.objects.get(username=request.POST["username"])

	except:
		return redirect("/signup")


	actual_pass=obj.password
	given_pass=request.POST["pass"]
	context={"username":obj.username}

	if actual_pass==given_pass:
		my_cookie  = request.COOKIES['session-cookie'] 
		
		#obj2=SetCookie123.objects.get(username=)
		SetCookie123.objects.filter(username=request.POST["username"]).update(cookie_id_allocated=my_cookie)
		# obj2.cookie_id_allocated=my_cookie
		# obj2.refresh_from_db()
		return render(request,"dropbox3.html",{"my_username":request.POST["username"],"var":'user'})

	else:
		return render(request,"index.html",{"error_msg":"Wrong username/password combo"})
		#return redirect("/")
	
	

def signupcreation(request,*args):
	kwargs=request.POST
	context={"Name":kwargs["fullname"],"username":kwargs["username"],"email":kwargs["email"],"password":kwargs["pass"],"mobile":kwargs["mobile"]}
	User.objects.create(Name=kwargs["fullname"],username=kwargs["username"],email=kwargs["email"],password=kwargs["pass"],mobile=kwargs["mobile"])
	SetCookie123.objects.get_or_create(username=kwargs["username"],cookie_id_allocated="")
	os.system(f"hadoop fs -mkdir /{context['username']}")
	os.mkdir(f"D:/files_uploaded/{context['username']}")
	os.mkdir(f"C:/files_uploaded/{context['username']}")
	return redirect('/')


def return_username_from_cookie(request):
	if "session-cookie" in request.COOKIES:
		cookie_obtained=request.COOKIES['session-cookie'] 
		try:
			obj= SetCookie123.objects.get(cookie_id_allocated=cookie_obtained)
			username_obtained=obj.username
			return username_obtained

		except:
			return None
	else:
		return None