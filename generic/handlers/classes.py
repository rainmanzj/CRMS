from startX.serivce.v1 import StartXHandler, get_datetime_format, get_m2m_display, StartXModelForm
from generic import models
from startX.forms.widgets import DateTimePickerInput
from startX.serivce.v1 import Option


class ClassesModelForm(StartXModelForm):
    class Meta:
        model = models.Classes
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput
        }


class ClassesHandler(StartXHandler):
    model_form_class = ClassesModelForm

    def display_course(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '班级'
        return '%s(%s期)' % (model.course.name, model.semester)

    list_display = ['school', display_course, get_datetime_format('开班日期', 'start_date'), 'class_teacher',
                    get_m2m_display('任课老师', 'tech_teachers'), 'price']

    search_list = ['course__contains', 'semester__contains', 'school__contains']
    search_group = [
        Option('school'),
        Option('course'),

    ]
