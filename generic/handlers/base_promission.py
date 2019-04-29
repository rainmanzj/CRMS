#!/usr/bin/env python
# -*- coding:utf-8 -*-


class PermissionHandler(object):

    # 是否显示添加按钮
    def get_add_btn(self, request, *args, **kwargs):
        from django.conf import settings
        # 当前用户所有的权限信息
        permission_dict = request.session.get(settings.INIT_PERMISSION)
        # 判断url有没有分发前缀
        if has_namespace(self, self.get_add_name) not in permission_dict:
            return None

        return super().get_add_btn(request, *args, **kwargs)

    # 是否显示编辑和删除按钮
    def get_list_display(self, request, *args, **kwargs):
        from django.conf import settings
        # 当前用户所有的权限信息
        permission_dict = request.session.get(settings.INIT_PERMISSION)
        value = []
        if self.list_display:
            value.extend(self.list_display)
            if has_namespace(self, self.get_change_name) in permission_dict and has_namespace(self,
                                                                                              self.get_del_name) in permission_dict:
                value.append(type(self).display_edit_del)
            elif has_namespace(self, self.get_change_name) in permission_dict:
                value.append(type(self).display_edit)
            elif has_namespace(self, self.get_del_name) in permission_dict:
                value.append(type(self).display_del)
        return value


def has_namespace(obj, func):
    """

    :param obj: 当前的对象
    :param func: 该对象对应的url方法
    :return: 判断url路由是否有分发前缀 如：startX:XX，如果有前缀返回前缀,如果没有前缀直接返回别名
    """
    if not obj.site.namespace:
        return func
    else:
        return '%s:%s' % (obj.site.namespace, func)
