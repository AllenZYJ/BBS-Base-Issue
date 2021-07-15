from django.shortcuts import render
from ghapi.all import GhApi
from ghapi.core import *
import os
from fastcore.test import *
from nbdev.showdoc import *
import difflib
from fastcore.nb_imports import *
from bbs_v01 import models as DATABASE
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
GITHUBTOKEN="your github_token"
REPO_BBS='your repo'
OWNER_BBS='your github name'
def GET_GITHUB():
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    return api
def New_Issue(request):
    api=GET_GITHUB()
    user_id=request.COOKIES.get('user_id')
    print(user_id)
    is_login=request.COOKIES.get('is_login')
    labels=[]
    # print(user_label)
    if is_login:
        try:
            new_issue_title=request.POST['new_issue_title']
            new_issue_body=request.POST['new_issue_body']
            new_issue_labels=request.POST['new_issue_labels']
            for label in new_issue_labels.split(","):
                labels.append(label)
            print(labels)
            print("ok",new_issue_title,new_issue_body,new_issue_labels)
            # 存在label中userid被自动同化问题
            issue = api.issues.create(owner=OWNER_BBS, repo=REPO_BBS,title=new_issue_title,labels=labels,body=new_issue_body)
            DATABASE.USER_ISSUES.objects.create(issue_id=issue.number,user_id=user_id)
            DATABASE.TITLE_BODY.objects.create(title=new_issue_title,body=new_issue_body,issue_id=issue.number,user_id=user_id)

            print(issue)
            return render(request, 'page-create-topic.html',context={'login_state':"发表成功，请回到首页查看"})
        except:
            return render(request, 'page-create-topic.html',context={'login_state':"未输入内容"})

    return render(request, 'page-create-topic.html',context={'login_state':"（未登录）"})

def transform_issue(raw_issuess_info):
    Disscuss_Info=[]
    discuss_length=len(raw_issuess_info)
    for idx in range(discuss_length):
        dict_issuess=dict(raw_issuess_info.__getitem__(idx))
        Disscuss_Info.append(dict_issuess)
    return Disscuss_Info
def get_issue_list():
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    flag="continue"
    return_list=[]
    num_page=1
    while flag=="continue":
        issuessss=api.issues.list_for_repo(owner=OWNER_BBS, repo=REPO_BBS,per_page=10,page=num_page)
        all_issues=transform_issue(issuessss)
        list_result=transform_issue(all_issues)
        if len(list_result)==0:
            flag="no-continue"
            print("num_page:",num_page)
        else:
            for single_issue in list_result:
                return_list.append(single_issue)
            num_page+=1
    print(len(return_list))
    return return_list
def get_issue_list_form_list(list_toget):
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    issues_from_list=[]
    for issue_id in list_toget:
        issue=api.issues.get(owner=OWNER_BBS, repo=REPO_BBS,issue_number=issue_id)
        issues_from_list.append(issue)
    # print(issues_from_list)
    return issues_from_list
def Discuss_List(request):
    # print(request.COOKIES.get('is_login'))
    status = request.COOKIES.get('is_login')
    user_id=request.COOKIES.get('user_id')
    # print("当前状态：",status)
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    # issuessss=api.issues.list_for_repo(owner=OWNER_BBS, repo=REPO_BBS)
    all_issues=get_issue_list()
    # print(to_index_context)
    paginator = Paginator(all_issues, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html',context={'data':page_obj,'user_id':user_id,'page_obj': page_obj})
def Discuss_List2(request):
    # clear_database_rewrite(request)
    # print(request.COOKIES.get('is_login'))
    status = request.COOKIES.get('is_login')
    user_id=request.COOKIES.get('user_id')
    # print("当前状态：",status)
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    # issuessss=api.issues.list_for_repo(owner=OWNER_BBS, repo=REPO_BBS)
    all_issues=get_issue_list()
    print(all_issues)
    # print(to_index_context)
    # print(all_issues[0])
    paginator = Paginator(all_issues, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for single_topic in page_obj:
        issue_obj=DATABASE.USER_ISSUES.objects.filter(issue_id=single_topic['number']).first()
        if issue_obj:
            admin_user_id=issue_obj.user_id
        else:
            admin_user_id="unknown user"
        labels_list=[]
        for single_label in single_topic['labels']:
            # print("labels",single_label['name'])
            labels_list.append(single_label['name'].split("-"))
        single_topic["labels_name"]=labels_list
        single_topic["admin_user_id"]=admin_user_id
    # print("page_obj",page_obj[-1]["labels_name"])
    return render(request, 'index_v3.html',context={'data':page_obj,'user_id':user_id,'page_obj': page_obj})
def Generate_Detail(request,number):
    username = request.COOKIES.get('user_id')
    flag_primission = 0
    if username!=None:
        print(request.COOKIES.get('is_login'))
        flag_primission=0
        try:
            comment_to_submit=request.POST['comment']
        except:
            comment_to_submit=0
        try:
            new_body=request.POST['new_body']
            print("body",len(new_body))
            if len(new_body)>1:
                new_body=1
        except:
            new_body=0
        try:
            new_title=request.POST['new_title']
            print("title",len(new_title))
            if len(new_title)>1:
                new_title=1
        except:
            new_title=0
        github_token=GITHUBTOKEN
        api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
        labels=api.issues.list_labels_on_issue(owner=OWNER_BBS, repo=REPO_BBS,issue_number=number)
        admin_obj=DATABASE.USER_ISSUES.objects.filter(issue_id=number).first()
        admin_user_name=admin_obj.user_id
        print("admin_user_name",admin_user_name)
        # print(labels)
        # print(transform_issue(labels)[0]['name']==request.COOKIES.get('user_id'))
        if admin_user_name==username:
            flag_primission = 1
        if new_title==1 and flag_primission==1:
            api.issues.update(owner=OWNER_BBS, repo=REPO_BBS, issue_number=number,title=request.POST['new_title'])
        if new_body==1 and flag_primission==1:
            api.issues.update(owner=OWNER_BBS, repo=REPO_BBS, issue_number=number,body=request.POST['new_body'])
        # issuessss=api.issues.list_for_repo(owner=OWNER_BBS, repo=REPO_BBS)
        all_issues=get_issue_list()
        for single_issue in all_issues:
            if single_issue['number']==number:
                details_issue=single_issue
                break
        if comment_to_submit!=0 and request.COOKIES.get('is_login'):
            print(request.POST['comment'])
            new_comments=api.issues.create_comment(owner=OWNER_BBS, repo=REPO_BBS,issue_number=number,body=request.POST['comment'])
            DATABASE.COMMENT_USER.objects.create(comment_id=new_comments.id,user_id=username,admin_id=admin_user_name)
        raw_comments=api.issues.list_comments(owner=OWNER_BBS, repo=REPO_BBS,issue_number=number)
        all_comments=transform_issue(raw_comments)
        for comments in all_comments:
            try:
                comment_info = DATABASE.COMMENT_USER.objects.filter(comment_id=comments['id']).first().user_id
            except:
                comment_info = "Unknown User"
            comments['user_name']=comment_info
        paginator = Paginator(all_comments, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        comment_page_obj = paginator.get_page(page_number)
        return_page=render(request, 'page-single-topic.html',context={'issue_number':number,'title':details_issue['title'],'body':single_issue['body'],'discuss_admin':admin_user_name,'comments':comment_page_obj,'page_obj': comment_page_obj,'condition':flag_primission,'user_id':username,"flag_primission":flag_primission})
    else:
        return_page=render(request,"page-login.html",context={'login_context':"访问议题请先登录"})
    return return_page
def New_Discuss(request):
    title = request.POST['title']
    body = request.POST['body']
    github_token=GITHUBTOKEN
    user_id=request.COOKIES.get('user_id')
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    issue = api.issues.create(title,labels=[user_id],body=body)#创建issue
    DATABASE.USER_ISSUES.objects.create(issue_id=issue.id,user_id=user_id)
    DATABASE.TITLE_BODY.objects.create(title=title,body=body,issue_id=issue.id,user_id=user_id)
    return render(request, 'discuss_detail.html',context={'title':title,'body':body})
def Register(request):
    return render(request, 'page-signup.html')
def Register_Succeed(request):
    user_id=request.POST['user_id']
    password=request.POST['password']
    print(user_id,password)
    user_repeat = DATABASE.USER_DATA.objects.filter(user_id=user_id).count()
    print(user_repeat)
    if user_repeat==0:
        DATABASE.USER_DATA.objects.create(user_id=user_id,password=password)
        return render(request, 'register_success.html')
    else:
        return render(request, 'register_fail.html')
def UpDate(request):
    print(request.COOKIES.keys())
    print(request.POST['new_title'])
    print(request.POST['new_body'])
    return render(request, 'page-login.html',context={'login_context':"欢迎来到iBooker"})
def login(request):
    return render(request, 'page-login.html',context={'login_context':"欢迎来到iBooker"})
def To_Login(request):
    username = request.POST.get("username")
    password = request.POST.get("pwd")
    print(username, password)
    user_obj = DATABASE.USER_DATA.objects.filter(user_id=username, password=password).first()
    # print(user_obj.user_id)
    if not user_obj:
        return render(request, 'page-login.html')
    else:
        # rep = render(request, 'index_v3.html',context={'data':page_obj,'user_id':user_id,'page_obj': page_obj})
        rep = redirect("/index_v3/",context={'user_id':'page_obj'})
        rep.set_cookie("is_login", True)
        rep.set_cookie("user_id",user_obj.user_id)
        return rep
def Logout(request):
    rep = redirect('/login/')
    rep.delete_cookie("is_login")
    rep.delete_cookie("user_id")
    rep.delete_cookie("csrftoken")
    print(request.COOKIES)
    return rep
def DeleteIssue(request,issue_number):
    username=request.COOKIES.get('user_id')
    api=GET_GITHUB()
    flag_primission=0
    labels=api.issues.list_labels_on_issue(owner=OWNER_BBS, repo=REPO_BBS,issue_number=issue_number)
    admin_obj=DATABASE.USER_ISSUES.objects.filter(issue_id=issue_number).first()
    admin_user_name=admin_obj.user_id
    if admin_user_name==username:
        flag_primission=1
    if  flag_primission==1:        
        api.issues.update(owner=OWNER_BBS, repo=REPO_BBS, issue_number=issue_number,title="Deleted",body="Deleted")
    print("issue_number",issue_number)
    rep = redirect("/details/"+str(issue_number))
    return rep
def Delete_Comment(request,issue_number,comment_number):
    username=request.COOKIES.get('user_id')
    api=GET_GITHUB()
    comment_delete_obj = DATABASE.COMMENT_USER.objects.filter(comment_id=comment_number,user_id=username).first()
    admin_delete_obj=DATABASE.COMMENT_USER.objects.filter(comment_id=comment_number,admin_id=username).first()
    print("comment_delete_obj",comment_delete_obj)
    print(admin_delete_obj)
    if comment_delete_obj or admin_delete_obj:
        api.issues.delete_comment(owner=OWNER_BBS, repo=REPO_BBS,comment_id=comment_number)
    rep = redirect("/details/"+str(issue_number))
    return rep
def clear_database_rewrite(request):
    issues_list=get_issue_list()
    print(issues_list)
    DATABASE.TITLE_BODY.objects.all().delete()
    for issue in issues_list:
        title_towrite=issue['title']
        body_towrite=issue['body']
        issue_number=issue['number']
        user_id=DATABASE.USER_ISSUES.objects.filter(issue_id=issue_number).first()
        if title_towrite==None:
            title_towrite="Nothing"
        if body_towrite==None:
            body_towrite="Nothing"
        if user_id==None:
            user_id_towrite="admin"
        else:
            user_id_towrite=user_id.user_id
        # print(title_towrite,body_towrite,issue_number,user_id_towrite)
        DATABASE.TITLE_BODY.objects.create(title=title_towrite,body=body_towrite,issue_id=issue_number,user_id=user_id_towrite)
    return 0
def Search_Result(request):
    keyword=request.POST.get("keyword")
    title_body=DATABASE.TITLE_BODY.objects.all()
    all_title={}
    output_list_title=[]
    topline=0.0
    issuesid_list=[]
    for single_issue in title_body:
        diff_score=difflib.SequenceMatcher(None,single_issue.title,keyword).ratio()
        all_title[diff_score]=[]
    for single_issue in title_body:
        diff_score=difflib.SequenceMatcher(None,single_issue.title,keyword).ratio()
        all_title[diff_score].append(single_issue.title)
        all_title[diff_score].append(single_issue.issue_id)
    for title_list_to_compare in sorted(all_title,reverse=True):
        for title in all_title[title_list_to_compare]:
            output_list_title.append(title)
    for index in range(1,len(output_list_title),2):
        issuesid_list.append(int(output_list_title[index]))
    print(issuesid_list)
    issues_from_list=get_issue_list_form_list(issuesid_list[:10])
    print(issues_from_list)
    # ----------------------------------------
    status = request.COOKIES.get('is_login')
    user_id=request.COOKIES.get('user_id')
    github_token=GITHUBTOKEN
    api = GhApi(owner=OWNER_BBS, repo=REPO_BBS, token=github_token)
    for single_topic in issues_from_list:
        issue_obj=DATABASE.USER_ISSUES.objects.filter(issue_id=single_topic['number']).first()
        if issue_obj:
            admin_user_id=issue_obj.user_id
        else:
            admin_user_id="unknown user"
        labels_list=[]
        for single_label in single_topic['labels']:
            labels_list.append(single_label['name'].split("-"))
        single_topic["labels_name"]=labels_list
        single_topic["admin_user_id"]=admin_user_id
    return render(request,"page-search_list.html",context={'data':issues_from_list,'user_id':user_id})