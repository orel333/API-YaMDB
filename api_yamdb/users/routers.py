<<<<<<< HEAD
from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomRouter(SimpleRouter):
    routes = [  # try tuple
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-base',
            detail=False,
            initkwargs={'suffix': 'users-list'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'user-detail'}
        )
=======
from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomRouter(SimpleRouter):
    routes = [  # try tuple
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-base',
            detail=False,
            initkwargs={'suffix': 'users-list'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'user-detail'}
        )
>>>>>>> master
    ]