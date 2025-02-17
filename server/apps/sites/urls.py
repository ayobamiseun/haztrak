from django.urls import include, path

from apps.sites.views import (  # type: ignore
    HandlerSearchView,
    RcraSiteView,
    SiteDetailView,
    SiteListView,
    SiteSearchView,
)

urlpatterns = [
    path(
        "rcra/",
        include(
            [
                path("handler/search", HandlerSearchView.as_view()),
                path("handler/<int:pk>", RcraSiteView.as_view()),
            ]
        ),
    ),
    # Site
    path("site", SiteListView.as_view()),
    path("site/search", SiteSearchView.as_view()),
    path("site/<str:epa_id>", SiteDetailView.as_view()),
]
