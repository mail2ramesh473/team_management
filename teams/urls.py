from django.conf.urls import url
from teams.views import add_team_member, update_team_member, delete_team_memeber


urlpatterns = [
    url(r'add/$',add_team_member),
    url(r'update/$',update_team_member),
    url(r'delete/$', delete_team_memeber)

]
