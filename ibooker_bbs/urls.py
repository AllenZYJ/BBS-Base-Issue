"""ibooker_bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
# from firstweb import views
from bbs_v01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/',views.Discuss_List2),
    path('details/<int:number>',views.Generate_Detail),
    path('details/delete_issue/<int:issue_number>',views.DeleteIssue),
    path('details/delete_comment/<int:issue_number>_<int:comment_number>',views.Delete_Comment),
    url(r'^login', views.login),
    url(r'^update', views.UpDate),
    url(r'^delete_issue', views.DeleteIssue),
    url(r'^index',views.Discuss_List2),
    url(r'^new',views.New_Issue),
    url(r'^to_login', views.To_Login),
    url(r'^logout',views.Logout),
    url(r'^new_discuss',views.New_Discuss),
    url(r'^register_succeed',views.Register_Succeed),
    url(r'^register',views.Register),
    url(r'^search_result',views.Search_Result)
    # url(r'^calpage',views.calpage),
    # url(r'^cal_list',views.cal_list),
    # url(r'^cal',views.cal)
]
