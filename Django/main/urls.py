from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('robots', views.RobotIndex.as_view(), name='robotindex'),
    path('robots/<int:pk>', views.RobotDetailView.as_view(), name='robotdetail'),
    path('events', views.IndexView.as_view(), name='eventview'),
    path('events/<int:pk>', views.EventDetailView.as_view(), name='eventdetail'),
    path('contests/<int:contest_id>/signup', views.contestSignup, name='contestsignup'),
    path('myteams', views.myteamsview, name='myteams'),
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='teamdetail'),
    path('accounts/register', views.register, name='register'),
]
