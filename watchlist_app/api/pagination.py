from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 3
    # page_query_param='p' #if you wish to rename default param: page=2
    page_size_query_param='size' #client can specify how big the page size they want to load
    max_page_size = 10 #upper limit that client can  specify
    # last_page_strings='end' #overwrites page=last that helps gets the last page
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit=5
    max_limit=10

#we can do next and previous but we cannot go to a definate page number as in page related    
#useful in agreement kind of pages so that client must visit all page and next
class WatchListCPagination(CursorPagination):  
    page_size = 5
    ordering ='created' # default is -created
