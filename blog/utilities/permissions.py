#------permission are classified into three types------->
#first-level:-Admin,Superadmin,Superuser (this is  user model class which can be considered as ObjectA)
#second-level:-object 'B' is assigned to user(i.e in object B , ObjectA is assigned), where user called as ObjectA
#third-level:-object 'C' is assigned to object object B(i.e object B is assigned in object C)

#model ObjectB->user field
#model ObjectC->objectB field(objectB id)


#as example, we can consider as , user,company,job where user is ObjectA,company is ObjectB,job is ObjectC

from rest_framework.permissions import BasePermission

SUPER_ADMIN = 1
ADMIN = 2


def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def SuperAdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.is_superuser)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.is_staff)

def allAdminLevel(request):
    return bool(SuperAdminLevel(request) or AdminLevel(request))

def isOwner(request):
    if str(request.user.id) == str(request.data.get('user')):
        return True
    
    elif len(request.data)==0 and len(request.POST)==0:
        return True

    return False


# def ObjectBOwner(request):
#     company = ObjectB.objects.filter(id = request.data.get('objectb'),user = request.user.id)
#     if company.exists():
#         return True
#     return False

# class blogPermission(BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ["list"]:
#             return True
#         elif view.action in ['retrieve']:
#             return True
#         elif view.action in ['create','update']:
#             return SuperAdminLevel(request) or AdminLevel(request) or isOwner(request)            
#         elif view.action == "partial_update":
#             return view.get_object().user_id == request.user.id
#         elif view.action == 'destroy':
#             return isOwner(request)


# class blogCategoryPermission(BasePermission):
#     def has_permission(self, request, view):    
#         if view.action in ["list"]:
#             return request.user.has_perm('blog.view_blogcategory')
#         elif view.action in ['retrieve']:
#             return request.user.has_perm('blog.view_blogcategory')
#         elif view.action in ['create']:
#             return request.user.has_perm('blog.add_blogcategory') and allAdminLevel(request)
#         elif view.action in ['partial_update','update']:
#             return request.user.has_perm('blog.change_blogcategory') and allAdminLevel(request)
#         elif view.action == 'destroy':
#             return request.user.has_perm('blog.delete_blogcategory')
class blogPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow list action for all users
        if view.action == "list":
            return True

        # Define static permissions for each action and each model
        permissions = {
            "retrieve": [
                "blog.view_blog",
                "blog.view_blogtags",
                "blog.view_blogcategory",
            ],
            "create": [
                "blog.add_blog",
                "blog.add_blogtags",
                "blog.add_blogcategory",
            ],
            "update": [
                "blog.change_blog",
                "blog.change_blogtags",
                "blog.change_blogcategory",
            ],
            "partial_update": [
                "blog.change_blog",
                "blog.change_blogtags",
                "blog.change_blogcategory",
            ],
            "destroy": [
                "blog.delete_blog",
                "blog.delete_blogtags",
                "blog.delete_blogcategory",
            ],
        }

        # Check if the action has a corresponding permission defined
        if view.action in permissions:
            # User must have at least one of the permissions for the action
            return any(request.user.has_perm(perm) for perm in permissions[view.action])

        # Default to denying permission if action does not match any predefined keys
        return False
