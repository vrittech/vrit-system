from rest_framework.routers import DefaultRouter
from ..viewsets.blogtags_viewsets import blogtagsViewsets
from ..viewsets.blog_viewsets import blogViewsets
from ..viewsets.blogcategory_viewsets import blogcategoryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('blogtags', blogtagsViewsets, basename="blogtagsViewsets")
router.register('blogcategory', blogcategoryViewsets, basename="blogcategoryViewsets")
router.register('blog', blogViewsets, basename="blogViewsets")
