from startX.serivce.v1 import StartXHandler, get_datetime_format, get_m2m_display, StartXModelForm
from generic import models
from startX.forms.widgets import DateTimePickerInput
from startX.serivce.v1 import Option
from django.urls import reverse
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class ClassesModelForm(StartXModelForm):
    class Meta:
        model = models.Classes
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput
        }


class ClassesHandler(PermissionHandler,StartXHandler):
    model_form_class = ClassesModelForm

    def display_course(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '班级'
        return '%s(%s期)' % (model.course.name, model.semester)

    def display_classes_record(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '上课记录'
        record_url = reverse('startX:generic_courserecord_list', kwargs={'class_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">上课记录</a>' % record_url)

    list_display = ['school', display_course, get_datetime_format('开班日期', 'start_date'), 'class_teacher',
                    display_classes_record,
                    get_m2m_display('任课老师', 'tech_teachers'), 'price']

    search_list = ['course__contains', 'semester__contains', 'school__contains']
    search_group = [
        Option('school'),
        Option('course'),

    ]
