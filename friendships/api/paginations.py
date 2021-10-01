from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FriendshipPagination(PageNumberPagination):
    # 默认的 page size，也就是 page 没有在 url 参数里的时候
    page_size = 20
    # 默认 page_size_query_param 是 None 表示不允许客户端指定每一页的大小
    page_size_query_param = 'size'
    # 允许客户端指定的最大 page_size 是多少
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'has_next_page': self.page.has_next(),
            'results': data,
        })
