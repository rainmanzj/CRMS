from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm
from django.urls import re_path
from generic import models
from django.shortcuts import HttpResponse
from django import forms
from .base_promission import PermissionHandler


class PaymentRecordModelForm(StartXModelForm):
    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'classes', 'note']


class StudentPaymentRecordModelForm(StartXModelForm):
    qq = forms.CharField(label='QQ号', max_length=32)
    mobile = forms.CharField(label='手机号', max_length=32)
    emergency_contract = forms.CharField(label='紧急联系人电话', max_length=32)

    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'classes', 'qq', 'mobile', 'emergency_contract', 'note']


class PayMentHandler(PermissionHandler, StartXHandler):
    list_display = ['customer', get_field_display('缴费类型', 'pay_type'), 'paid_fee', 'classes', 'consultant',
                    get_field_display('状态', 'confirm_status')]
    model_form_class = PaymentRecordModelForm

    def get_list_display(self, request, *args, **kwargs):
        """
        获取页面上应该显示的列，预留的自定义扩展，例如：以后根据用户的不同显示不同的列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_model_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_consultant_id)

    def get_model_form(self, is_add, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        student_object = models.Student.objects.filter(customer_id=customer_id).exists()
        if not student_object:
            return StudentPaymentRecordModelForm
        return PaymentRecordModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']

        object_exists = models.Customer.objects.filter(id=customer_id,
                                                       consultant_id=current_consultant_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')
        # 缴费记录
        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_consultant_id
        form.save()

        # 创建学员信息
        classes = form.cleaned_data['classes']
        fetch_student_object = models.Student.objects.filter(customer_id=customer_id).first()
        if not fetch_student_object:
            qq = form.cleaned_data['qq']
            mobile = form.cleaned_data['mobile']
            emergency_contract = form.cleaned_data['emergency_contract']
            student_object = models.Student.objects.create(customer_id=customer_id, qq=qq, mobile=mobile,
                                                           emergency_contract=emergency_contract)
            student_object.classes.add(classes.id)
        else:
            fetch_student_object.classes.add(classes.id)
