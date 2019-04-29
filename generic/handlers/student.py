from startX.serivce.v1 import StartXHandler, get_field_display, get_m2m_display, Option
from django.urls import re_path
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class StudentHandler(PermissionHandler, StartXHandler):

    def display_score(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '积分管理'
        record_url = reverse('startX:generic_scorerecord_list', kwargs={'student_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (record_url, model.score))

    list_display = ['customer', 'qq', 'mobile', 'emergency_contract', get_m2m_display('所报班级', 'classes'),
                    display_score, get_field_display('学员状态', 'student_status'), 'memo']

    def get_add_btn(self, request, *args, **kwargs):
        return

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    search_list = ['customer__name__contains', 'qq__contains', 'mobile__contains', ]
    search_group = [
        Option('classes', text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    ]
