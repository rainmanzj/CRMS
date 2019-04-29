from startX.serivce.v1 import StartXHandler
from .base_promission import PermissionHandler


class CourseHandler(PermissionHandler, StartXHandler):
    list_display = ['name']
