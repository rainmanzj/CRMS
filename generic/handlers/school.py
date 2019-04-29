from startX.serivce.v1 import StartXHandler
from .base_promission import PermissionHandler


class SchoolHandler(PermissionHandler, StartXHandler):
    list_display = ['title']
