from startX.serivce.v1 import StartXHandler, get_field_display
from .base_promission import PermissionHandler


class HomeworkHandler(PermissionHandler, StartXHandler):
    list_display = ['student', 'classes', 'courses', 'content', 'teacher', get_field_display('作业状态', 'status')]
