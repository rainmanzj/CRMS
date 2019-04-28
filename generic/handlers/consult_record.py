from startX.serivce.v1 import StartXHandler, StartXModelForm, get_m2m_display
from django.urls import re_path
from generic import models
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe


class ConsultRecordModelForm(StartXModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = ['note', ]


class ConsultRecordHandler(StartXHandler):
    list_display = ['note', 'consultant', 'date']
    list_template = 'consult_record.html'
    model_form_class = ConsultRecordModelForm

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_del_name)

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_model_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_consultant_id)

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']

        object_exists = models.Customer.objects.filter(id=customer_id,
                                                       consultant_id=current_consultant_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')

        if not is_update:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_consultant_id

        form.save()

    def display_edit_del(self, model=None, is_header=None, *args, **kwargs):

        if is_header:
            return '操作'
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=model.pk, customer_id=customer_id),
            self.reverse_delete_url(pk=model.pk, customer_id=customer_id))
        return mark_safe(tpl)

    def get_change_object(self, request, pk, *args, **kwargs):

        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']
        return models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                   customer__consultant_id=current_consultant_id).first()

    def get_delete_object(self, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']
        record_queryset = models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                              customer__consultant_id=current_consultant_id)

        if not record_queryset.exists():
            return HttpResponse('要删除的记录不存在，请重新选择！')
        record_queryset.delete()
