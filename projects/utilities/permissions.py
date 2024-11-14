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
    return bool(IsAuthenticated(request) and request.user.role in [ADMIN,SUPER_ADMIN])

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

# class projectsPermission(BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ["list"]:
#             return True
#         elif view.action in ['retrieve']:
#             return isOwner(request)
#         elif view.action in ['create','update']:
#             return isOwner(request) #second level
#             return ObjectBOwner(request) #third level
#         elif view.action == "partial_update":
#             return view.get_object().user_id == request.user.id
#         elif view.action == 'destroy':
#             return isOwner(request)
from rest_framework.permissions import BasePermission

class projectsPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow list action for all users
        if view.action == "list":
            return True

        # Define permissions for each action statically for each model
        permissions = {
            "retrieve": [
                "projects.view_project",
                "projects.view_projectgroup",
                "projects.view_projectservice",
                "projects.view_projectlink",
            ],
            "create": [
                "projects.add_project",
                "projects.add_projectgroup",
                "projects.add_projectservice",
                "projects.add_projectlink",
            ],
            "update": [
                "projects.change_project",
                "projects.change_projectgroup",
                "projects.change_projectservice",
                "projects.change_projectlink",
            ],
            "partial_update": [
                "projects.change_project",
                "projects.change_projectgroup",
                "projects.change_projectservice",
                "projects.change_projectlink",
            ],
            "destroy": [
                "projects.delete_project",
                "projects.delete_projectgroup",
                "projects.delete_projectservice",
                "projects.delete_projectlink",
            ],
        }

        # Check permissions based on action
        if view.action in permissions:
            # User must have at least one of the permissions for the action
            return any(request.user.has_perm(perm) for perm in permissions[view.action])

        # Default to denying permission if action does not match any predefined keys
        return False

