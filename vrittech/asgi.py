# # """
# # ASGI config for vrittech project.

# # It exposes the ASGI callable as a module-level variable named ``application``.

# # For more information on this file, see
# # https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# # """

# # import os

# # from django.core.asgi import get_asgi_application

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vrittech.settings')

# # application = get_asgi_application()




# """
# ASGI config for vrittech project.

# It exposes the ASGI callable as a module-level variable named ``application``.
# """

# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application
# print("ASGI module loaded!")

# # Import your websocket routing
# import notification.routing  # make sure this matches your app name

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vrittech.settings')
# django.setup()

# application = ProtocolTypeRouter({
#     # Handle traditional HTTP requests
#     "http": get_asgi_application(),

#     # Handle WebSocket connections
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             notification.routing.websocket_urlpatterns
#         )
#     ),
# })




import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 1️⃣ Set settings before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vrittech.settings')

# 2️⃣ Setup Django apps
django.setup()

# 3️⃣ Now safe to import anything that uses models
from notification.routing import websocket_urlpatterns
from notification.middleware import JWTAuthMiddleware

# 4️⃣ Define application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
