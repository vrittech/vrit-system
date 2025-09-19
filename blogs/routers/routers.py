from rest_framework.routers import DefaultRouter

from blogs.viewsets.blogs_viewsets import blogSEOSettingsViewsets, blogViewsets, blogsCategoryViewsets


router = DefaultRouter()
auto_api_routers = router


router.register('blog-category', blogsCategoryViewsets, basename="blogsCategoryViewsets")
router.register('blog', blogViewsets, basename="blogViewsets")
router.register('blog-seo-settings', blogSEOSettingsViewsets, basename="blogSEOSettingsViewsets")
