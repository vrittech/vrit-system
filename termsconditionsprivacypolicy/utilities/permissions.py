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

class privacyPolicyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            # Creating new object
            return request.user.has_perm('termsconditionsprivacypolicy.add_privacypolicy')

        if request.method in ['PUT', 'PATCH']:
            # Editing existing object
            return request.user.has_perm('termsconditionsprivacypolicy.change_privacypolicy')

        if request.method == 'DELETE':
            # Deleting object
            return request.user.has_perm('termsconditionsprivacypolicy.delete_privacypolicy')
        
        return SuperAdminLevel(request)
    
    

class termsConditionsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            # Creating new object
            return request.user.has_perm('termsconditionsprivacypolicy.add_termsconditions')

        if request.method in ['PUT', 'PATCH']:
            # Editing existing object
            return request.user.has_perm('termsconditionsprivacypolicy.change_termsconditions')

        if request.method == 'DELETE':
            # Deleting object
            return request.user.has_perm('termsconditionsprivacypolicy.delete_termsconditions')
        
        return SuperAdminLevel(request)
 