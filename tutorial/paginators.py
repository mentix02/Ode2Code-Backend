from rest_framework.pagination import PageNumberPagination


class RecentTutorialPaginator(PageNumberPagination):
    page_size = 12
