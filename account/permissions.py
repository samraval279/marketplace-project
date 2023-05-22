from rest_framework import permissions

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action in [
            'create', 'login', 'refresh_token',
            'forgot_password', 'reset_password',
            ]:
            return True
        elif view.action in [
            'retrieve', 'update', 'partial_update', 'destroy',
            'change_password'
            ]:
            return request.user.is_authenticated
        else:
            return False
        
class CategoryPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if view.action in [
            'list','retrieve'
        ]:
            return True
        elif view.action in [
            'create', 'update', 'partial_update', 'destroy'
        ]:
            return request.user.is_authenticated
        
        else:
            return False
        

class ServiceRequestPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if view.action in [
            'list','retrieve', 'destroy'
        ]:
            return request.user.is_authenticated
        elif view.action in [
            'create',  
        ]:
            return True
        
        else:
            return False