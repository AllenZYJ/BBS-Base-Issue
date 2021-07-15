# BBS-Base-Issue

> 作者：张一极
>
> 本项目后端基于github-issue服务，以及简易sql数据库结构，前端基于bootstrap框架搭建。

### 1.主页

信息来源：issue列表

​	获取方法

```Python
issuessss=api.issues.list_for_repo(owner='AllenZYJ', repo='test_bbs')
```

​	设计规则：

返回类型是<class 'fastcore.foundation.L'>

该类有个方法是`L.__getitem__`可以直接获取内容，作为一个可迭代对象：

```python
def transform_issue(raw_issuess_info):
    Disscuss_Info=[]
    discuss_length=len(issuessss)
    for idx in range(discuss_length):
        dict_issuess=dict(issuessss.__getitem__(idx))
        Disscuss_Info.append(dict_issuess)
    return Disscuss_Info
```

### 2.讨论主题详情

实现了获取issue列表后传入django后台渲染出对应内容网页呈现给用户。

点击标题后，进入新页面，渲染出一个新的主题页面:

```python
def Generate_Detail(request,number):
    github_token="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"
    api = GhApi(owner='AllenZYJ', repo='test_bbs', token=github_token)
    issuessss=api.issues.list_for_repo(owner='AllenZYJ', repo='test_bbs',labels='bug')
    to_index_context=transform_issue(issuessss)
    for single_issue in to_index_context:
        if single_issue['number']==number:
            details_issue=single_issue
            break
    return render(request, 'discuss_detail.html',context={'title':details_issue['title'],'body':single_issue['body']})
```

![image-20210523001431578](pic/image-20210523001431578.png)

详情：

![image-20210523001553595](pic/image-20210523001553595.png)

### 3.用户组织形式：

​	sqlite3单表实现用户的密码和用户id填写保存，每一次用户登录，登录后跳转首页，确定好首页讯息，暂定所有信息陈列展示，超过10条下一页。

已保存到sqlite3数据库的userdata表中，进行匹配即可。

通过cookie的user_id去匹配数据库内的相应数据，并且通过user_id去获取当前用户的user_id，完成发帖，评论，等其他动作。

完成了用户id去重，检测到重复id注册将不被通过。

确定大小写检测

### 4.议题权限组织形式：

​	暂定使用labels中取一个作为用户标签，写上用户id，匹配即可编辑删除等。

​	比如张三-id99887-issue_id7777拥有权限，当张三用户登录上以后点击编辑或者其他高级操作的时候，后台逻辑会进行比对，如果比对顺利，则顺利跳转issue_update函数。

### 5.交流方式：

提交comment，每一次提交一个新的comment，都可以同时输入内容，确定自己的评论所在issue，自己对某个issue下的某个评论有控制权，会在创建的同时写入sqlite数据库：

```python
api.issues.create_comment(owner='AllenZYJ', repo='test_bbs',issue_number=6,body="my first comment")#创建评论
```

[Parameters](https://docs.github.com/en/rest/reference/issues#create-an-issue-comment--parameters)

| Name           | Type    | In     | Description                                                 |
| :------------- | :------ | :----- | :---------------------------------------------------------- |
| `accept`       | string  | header | Setting to `application/vnd.github.v3+json` is recommended. |
| `owner`        | string  | path   |                                                             |
| `repo`         | string  | path   |                                                             |
| `issue_number` | integer | path   | issue_number parameter                                      |
| `body`         | string  | body   | **Required**. The contents of the comment.                  |

使用comment_id鉴别是否拥有对此comment的修改编辑权限：

```python
issues.update_comment(owner, repo, comment_id, body): Update an issue comment
issues.delete_comment(owner, repo, comment_id): Delete an issue comment
```

可以更新，或者删除评论。

数据库组织形式：comment_id，user_id。

每一次对某一个comment_id的comment提出编辑、删除等要求，进行数据库比对权限。

### 6.发起新讨论：

提交表单，表单内容为issue标题，issue内容，接口为创建issue接口。

细则：

> 1.每一位创建issue的作者，对当前issue有修改权利和删除评论的权利，用数据库记录每个用户的权利范围。
>
> 2.每一位创建issue的作者，作为当前楼主，可以添加label（标签），添加评论，在每一次添加标签的时候进行检查，从数据库中调出当前用户对这个issue是否拥有权限修改。

```python
api = GhApi(owner='AllenZYJ', repo='test_bbs', token=github_token)#初始化
issue = api.issues.create("Created second issue for ibooker_bbs",labels=['bugs','documents'])#默认api位置的issue，即仓库issue，labels的list代表issue的标签，即label，便于筛选
```

[Parameters](https://docs.github.com/en/rest/reference/issues#create-an-issue--parameters)

| Name        | Type                                 | In     | Description                                                  |
| :---------- | :----------------------------------- | :----- | :----------------------------------------------------------- |
| `accept`    | string                               | header | Setting to `application/vnd.github.v3+json` is recommended.  |
| `owner`     | string                               | path   |                                                              |
| `repo`      | string                               | path   |                                                              |
| `title`     | string or integer                    | body   | **Required**. The title of the issue.                        |
| `body`      | string                               | body   | The contents of the issue.                                   |
| `assignee`  | string or nullable                   | body   | Login for the user that this issue should be assigned to. *NOTE: Only users with push access can set the assignee for new issues. The assignee is silently dropped otherwise. **This field is deprecated.*** |
| `milestone` | string or integer or nullable        | body   | The `number` of the milestone to associate this issue with. *NOTE: Only users with push access can set the milestone for new issues. The milestone is silently dropped otherwise.* |
| `labels`    | array of strings or array of objects | body   | Labels to associate with this issue. *NOTE: Only users with push access can set labels for new issues. Labels are silently dropped otherwise.* |
| `assignees` | array of strings                     | body   | Logins for Users to assign to this issue. *NOTE: Only users with push access can set assignees for new issues. Assignees are silently dropped otherwise.* |

发起新的议题同时会传递user_id给后端，给对应的issue加上label，label名为用户id。

### 7.标签

上述方法使用创建过程中的issue.labels实现标签，如果用户后续需要添加标签，则通过add_labels实现，但是这个标签无颜色，作为后端实现可以，如果丰富的话，可以加上颜色，单独设置一个创建标签的方式。

创建标签，ghapi里面有create_label函数，可以指定颜色：

```python
issues.create_label(owner, repo, name, color, description): Create a label
```

实例：

```python
api.issues.create_label(owner='AllenZYJ', repo='test_bbs', name='Edge',color='5093F8',description='Edge strawberry')
```

![image-20210521214102739](./pic/image-20210521214102739.png)

[Parameters](https://docs.github.com/en/rest/reference/issues#create-a-label--parameters)

| Name          | Type   | In     | Description                                                  |
| :------------ | :----- | :----- | :----------------------------------------------------------- |
| `accept`      | string | header | Setting to `application/vnd.github.v3+json` is recommended.  |
| `owner`       | string | path   |                                                              |
| `repo`        | string | path   |                                                              |
| `name`        | string | body   | **Required**. The name of the label. Emoji can be added to label names, using either native emoji or colon-style markup. For example, typing `:strawberry:` will render the emoji ![:strawberry:](https://github.githubassets.com/images/icons/emoji/unicode/1f353.png). For a full list of available emoji and codes, see "[Emoji cheat sheet](https://github.com/ikatyang/emoji-cheat-sheet)." |
| `color`       | string | body   | The [hexadecimal color code](http://www.color-hex.com/) for the label, without the leading `#`. |
| `description` | string | body   | A short description of the label.                            |

### 8.搜索

搜索部分，通过search.[Search issues and pull requests](https://docs.github.com/en/rest/reference/search#search-issues-and-pull-requests)

> ### [Search issues and pull requests](https://docs.github.com/en/rest/reference/search#search-issues-and-pull-requests)
>
> Find issues by state and keyword. This method returns up to 100 results [per page](https://docs.github.com/rest/overview/resources-in-the-rest-api#pagination).
>
> When searching for issues, you can get text match metadata for the issue **title**, issue **body**, and issue **comment body** fields when you pass the `text-match` media type. For more details about how to receive highlighted search results, see [Text match metadata](https://docs.github.com/rest/reference/search#text-match-metadata).
>
> For example, if you want to find the oldest unresolved Python bugs on Windows. Your query might look something like this.
>
> ```
> q=windows+label:bug+language:python+state:open&sort=created&order=asc
> ```
>
> This query searches for the keyword `windows`, within any open issue that is labeled as `bug`. The search runs across repositories whose primary language is Python. The results are sorted by creation date in ascending order, which means the oldest issues appear first in the search results.

> - [search.issues_and_pull_requests](https://docs.github.com/rest/reference/search/#search-issues-and-pull-requests)(q, sort, order, per_page, page): *Search issues and pull requests*
> - [search.labels](https://docs.github.com/rest/reference/search/#search-labels)(repository_id, q, sort, order): *Search labels*

支持issue-body，comment-body，title的主题context的搜索和呈现，每页100个结果。

### 9.删除议题

无法通过github api实现，只能由管理员登录账户进行删除

设置一个标签，前端搜索到这个议题，标签含有Deleted不予展示即可。

### 10.分页议题

通过django自带分页器实现，每一次传入的page_obj用法一致：

分页方式：

1.在temprates的html模板中，加入页码：

```html
<div class="pagination">    <span class="step-links">        {% if page_obj.has_previous %}            <a href="?page=1">&laquo; first</a>            <a href="?page={{ page_obj.previous_page_number }}">previous</a>        {% endif %}        <span class="current">            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.        </span>        {% if page_obj.has_next %}            <a href="?page={{ page_obj.next_page_number }}">next</a>            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>        {% endif %}    </span></div>
```

2.在views.py中对应视图函数加入：

```python
paginator = Paginator(all_comments, 5) # Show 25 contacts per page.page_number = request.GET.get('page')comment_page_obj = paginator.get_page(page_number)
```

3.修改传入的context字典内容：

> ​	修改对应的all_comments传入，无缝修改即可，因为comment_page_obj类似于all_comments的子对象，修改后依然可迭代，且键值不变。
>
> ​	新增传入键为：'page_obj': comment_page_obj

### 11.编辑议题

实现了js判断传入变量，将变量换为权限标志即可。

输入框无法出现，跳转页面的话，无法实现comment_id的传递。

### 12.主题问题：

> 1.首先{% load static %}
>
> 2.setting.py里写明static与temprates同级目录的static路径
>
> 3.<link rel="stylesheet" href="{% static '/assets/bootstrap/css/bootstrap.min.css' %}"

### 13.模板改造计划

1、完成登录页改造

2、完成首页改造

3、完成详情页改造（discuss_detail）

4、完成注册页改造

5、完成编辑页改造，折叠，未做验证

6、需要update页面改造，无法通过textarea直接让后端获取内容，已解决

7、**redirect重定向：它不仅能根据URL重定向，还可以根据对象Object重定向和根据视图view重定向**，根据视图重定向的时候还可以传递额外的参数，可以直接传递原有参数，重定向新页面。

8、实现完善了评论功能和编辑功能，包括权限检查。

9、用户楼主具有整个讨论的管理权限，包括评论，主题部分，现有的删除逻辑，可以让用户和论主删除自己的评论，修改还未实现

10、现用一张数据库表来确定评论和所属讨论的id对应关系，comment_id,user_id,admin_id

11、设计new—discuss页面，完成信息传递，需要在匹配user_id的基础上进行post，如未登录，则跳转登录页面

12、完成主页标签传入设计，模板迭代更精细化。

13、issue的labels无序排列，需修改后端遍历形式即可，将user_id独立包装（待实现）

