"""Learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name="base"),
    path('admin/', admin.site.urls),
    path('student/', include('student.urls', namespace='student'), name='student'),
    path('tutor/create_profile', views.create_profile,name="create_profile"),
    path('tutor/dashboard', views.dashboard,name="dashboard"),
    path('tutor/Projects', views.projects,name="projects"),
    path('tutor/todo_list', views.todo_list,name="todo_list"),
    path('tutor/ticket', views.ticket,name="ticket"),
    path('tutor/bid_created', views.create_bid,name="bid_create"),
    path('student/dashboard', views.stu_dashboard,name="stu_dashboard"),
    path('student/Post_question', views.Post_question,name="postquestion"),
    path('student/ticket', views.stu_ticket,name="stu_ticket"),
    # path('student/bid', views.stu_bid,name="stu_bid"),
    # path('student/(?P<bid_id>[0-9]*)', views.stu_bid, name = "stu_bid"),
    path("student/<int:myid>", views.stu_bid, name='stu_bid'),
    path("student/bid_approve/",views.bid_approve,name='bid_approve'),
    path("logout/", views.logout_user, name='logout'),
    
    
    # path('tutor/login',views.authenticate())
]
