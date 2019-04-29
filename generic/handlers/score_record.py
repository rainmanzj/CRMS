from startX.serivce.v1 import StartXHandler, StartXModelForm
from django.urls import re_path
from generic import models
from .base_promission import PermissionHandler


class ScoreRecordModelForm(StartXModelForm):
    class Meta:
        model = models.ScoreRecord
        fields = ['content', 'score']


class ScoreRecordHandler(PermissionHandler, StartXHandler):
    list_display = ['student', 'content', 'score', 'user']
    model_form_class = ScoreRecordModelForm

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<student_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<student_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_list_display(self, request, *args, **kwargs):
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_queryset(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        return self.model_class.objects.filter(student_id=student_id)

    def save(self, request, form, is_update, *args, **kwargs):
        student_id = kwargs.get('student_id')
        current_consultant_id = request.session['staffinfo']['staff_id']

        form.instance.student_id = student_id
        form.instance.user_id = current_consultant_id
        form.save()

        # 实时更新积分数据
        score = form.instance.score
        if score > 0:
            form.instance.student.score += abs(score)
        else:
            form.instance.student.score -= abs(score)
        form.instance.student.save()
