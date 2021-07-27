from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from users.models import SetCookie123,User
import os
import shutil


class FileDescription():
	def __init__(self,file_url,file_name):
		self.file_url=file_url
		self.file_name=file_name


# Create your views here.
def home_view(request,*args,**kwargs):
	if return_username_from_cookie(request)==None: #cookie extract
		response= render(request,"index.html",{})
		response.set_cookie('session-cookie',get_random_string(length=32)) 
		return response

	else:
		return redirect('/user')


def userdetails_view(request,*args,**kwargs):
	if return_username_from_cookie(request) ==None:
			return redirect('/')
	else:
		username=return_username_from_cookie(request)

	return render(request,"ht.html",{"my_username":username})


def user_detail_update(request):
	cookie_obtained=request.COOKIES['session-cookie'] 
	obj= SetCookie123.objects.get(cookie_id_allocated=cookie_obtained)
	username_obtained=obj.username

	name=request.POST["name"]
	email=request.POST["email"]
	password=request.POST["psw"]

	User.objects.filter(username=username_obtained).update(Name=name,email=email,password=password)
	return redirect("/userdet")

def storage_view(request,*args,**kwargs):
	my_file=request.FILES["filename"]

	cookie_obtained=request.COOKIES['session-cookie'] 
	obj= SetCookie123.objects.get(cookie_id_allocated=cookie_obtained)
	username_obtained=obj.username
	


	handle_uploaded_file(my_file,username_obtained)
	return render(request,"success.html",{"my_username":username_obtained})

def file_list_view(request):
	if return_username_from_cookie(request) ==None:
			return redirect('/')
	else:
		username=return_username_from_cookie(request)
	all_file_names=os.listdir(f'D:/files_uploaded/{username}') + os.listdir(f'C:/files_uploaded/{username}')
	context={"all_files":[],"var":'file_view',"my_username":username}
	for file in all_file_names:
		file_url=f"/download/{username}/{file}"
		context["all_files"].append(FileDescription(file_url,file))


	return render(request,"fileview.html",context)

def log_out(request): 
	if return_username_from_cookie(request) ==None:
			return redirect('/')
	else:
		username=return_username_from_cookie(request)

	SetCookie123.objects.filter(username=username).update(cookie_id_allocated="")
	return redirect('/')






def file_rendering(request,username_from_url,filename_from_url):
	file_extension=filename_from_url[-3:]
	if filename_from_url in os.listdir(f"D:/files_uploaded/{username_from_url}/"):
		image_data = open(f"D:/files_uploaded/{username_from_url}/{filename_from_url}", "rb").read()

	else:
		image_data = open(f"C:/files_uploaded/{username_from_url}/{filename_from_url}", "rb").read()

	if file_extension=="png" or file_extension=="jpg" or file_extension=="jpeg":
		return HttpResponse(image_data, content_type=f"image/{file_extension}")

	elif file_extension=="pdf":
		return HttpResponse(image_data, content_type="application/pdf")

	elif file_extension=="mp4":	
		return HttpResponse(image_data, content_type="video/mp4")

	# return render(request,"fileview.html",{})
	else:
		return HttpResponse(image_data,content_type="application/octet-stream")


def dashboard_view_new(request):
	cookie_obtained=request.COOKIES['session-cookie'] 
	obj= SetCookie123.objects.get(cookie_id_allocated=cookie_obtained)
	username=obj.username

	one_gb_bytes=1073741824
	used = find_folder_size(f"D:/files_uploaded/{username}")
	used2= find_folder_size(f"C:/files_uploaded/{username}")

	total_used=used+used2
	print(total_used)
	percentage_used=(total_used / (0.5*one_gb_bytes))*100 #this means that 0.5GB is considered as storage full

	percentage_used=round(percentage_used,2)
	print(percentage_used)
	if percentage_used>=50:
		deg1=180
		deg2=(percentage_used-50)*3.6
	else:
		deg2=0
		deg1=3.6*percentage_used


	deg1=round(deg1)
	deg2=round(deg2)
	count_doc=0
	count_images=0
	count_videos=0
	list_of_files=os.listdir(f"D:/files_uploaded/{username}/") + os.listdir(f"C:/files_uploaded/{username}/")
	
	for file1 in list_of_files:
		print("testing file extension:",file1[-3:])
		if file1[-3:] =="pdf"or file1[-3:]=="ocx":
			count_doc+=1

		elif file1[-3:]=="mp4" or file1[-3:]=="mkv" or file1[-3:]=="avi":
			count_videos+=1

		elif file1[-3:]=="png" or file1[-3:]=="jpg" or file1[-3:]=="peg":
			count_images+=1

	
	context={"amount":round((total_used/one_gb_bytes)*10,2)  ,"deg1": deg1, "deg2":deg2,"my_username":username,"percentage_used":percentage_used,"var":'dashboard',"count_images":count_images,"count_doc":count_doc,"count_videos":count_videos}
	return render(request,"dash.html",context)

def signup_view(request,*args,**kwargs):
    return render(request,"signup.html",{})

def trash_view(request,trash_file):
	cookie_obtained=request.COOKIES['session-cookie'] 
	obj= SetCookie123.objects.get(cookie_id_allocated=cookie_obtained)
	username=obj.username
	if trash_file in os.listdir(f"D:/files_uploaded/{username}/"):
		os.remove(f"D:/files_uploaded/{username}/{trash_file}")

	else:
		os.remove(f"C:/files_uploaded/{username}/{trash_file}")
	os.system(f'hadoop fs -rm -R "/{trash_file}" /{username}')
	return redirect('/file_view')              	

def handle_uploaded_file(f,user): #load balance
	total, used, free = shutil.disk_usage("D:/")
	total2, used2, free2 = shutil.disk_usage("C:/")
	if free>=free2:
		drive_letter="D"

	else:
		drive_letter="G"

	with open(f'{drive_letter}:/files_uploaded/{user}/'+f.name, 'wb+') as destination:
		for chunk in f.chunks():  
			destination.write(chunk) 
	file_path=f'{drive_letter}:/files_uploaded/{user}/'+f.name
	print(f'hadoop fs -put "{file_path}" /{user}')
	os.system(f'hadoop fs -put "/{file_path}" /{user}')

def find_folder_size(start_path):

	total_size = 0
	for path, dirs, files in os.walk(start_path):
	    for f in files:
	        fp = os.path.join(path, f)
	        total_size += os.path.getsize(fp)
	return int(total_size)


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




#find all disk usage finding commands linux
#find the folder where hdfs stores files
#replace all D:? and C:? with os.system calls
#Link was generated based on file location; change it to hdfs link