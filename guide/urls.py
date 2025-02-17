from django.urls import path
from . import views
urlpatterns =[
    path('create-guide', views.CreateGuideView.as_view(), name='create-guide'),
    path('get-update-destroy-guide/<int:pk>', views.GetUpdateDestroyGuideView.as_view(), name='get-update-destroy-guide'),
    path('create-route/', views.CreateRouteView.as_view(), name='create-route'),
    path('get-update-destroy-route', views.GetUpdateDestroyRouteView.as_view(), name='get-update-destroy-route'),
    path('like-route/<int:route_id>/<int:user_id>', views.LikeRouteView.as_view(), name='like-route'),
    path('un-like-route/<int:route_id>/<int:user_id>', views.UnLikeRouteView.as_view(), name='un-like-route'),
    path('dislike-route/<int:route_id>/<int:user_id>', views.DisLikeRouteView.as_view(), name='dislike-route'),
    path('un-dislike-route/<int:route_id>/<int:user_id>', views.UnDisLikeRouteView.as_view(), name='un-dislike-route'),
    path('share-route/<int:route_id>/<int:user_id>', views.ShareRouteView.as_view(), name='share-route'),

]