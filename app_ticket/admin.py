import datetime
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.db import models
from app_ticket.models import Ticket, TicketType
from django.utils.html import format_html
from django.contrib.auth.models import User
from simpleui.admin import AjaxAdmin
from django.http import HttpResponse, JsonResponse

admin.site.site_header = "工单系统"
admin.site.site_title = "工单系统"


@admin.register(TicketType)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'type_name', 'ticket_title', 'is_auto',

    )
    actions = ('create_tpl', )

    def create_tpl(self, request, queryset):
        pass
    create_tpl.short_description = '创建工单模板'
    create_tpl.icon = 'el-icon-circle-plus'
    create_tpl.type = 'info'
    create_tpl.action_type = 0
    create_tpl.action_url = '/courier/ticket/add_tpl.html'

    def has_add_permission(self, request):
        pass

    def has_delete_permission(self, request, obj=None):
        pass
        # qs = super().has_delete_permission(request, obj=None)
        # if request.user.is_superuser:
        #     return qs

    def has_view_or_change_permission(self, request, obj=None):
        qs = super().has_view_or_change_permission(request, obj=None)
        if request.user.is_superuser:
            return qs
        # qs = super().has_delete_permission(request)
        # if request.user.is_superuser:
        #     return qs


@admin.register(Ticket)
class TicketAdmin(AjaxAdmin):

    list_display = (
        'id', 'ticket_type', 'ticket_title', 'format_detail', 'ticket_state', 'handle_time', 'op_id',  'create_by', 'create_time'

    )
    list_per_page = 10
    list_filter = ['active_type', 'ticket_type']
    readonly_fields = (
        'active_type',
        'app_code',
        'qa_id',
        'op_id',
        'create_by',
        'create_time',
        'close_time',
        'handle_time',
        'handle_result',
        'extra_params',
        'ticket_type',
        'ticket_title',
        'detail',
        'is_auto',
        'time_consuming',
    )
    search_fields = ['op_id', 'create_by']
    date_hierarchy = 'create_time'
    list_display_links = ('id', )
    actions = ('handle_confirm', 'add_ticket')

    def add_ticket(self, request, queryset):
        pass
    add_ticket.short_description = '创建新工单'
    add_ticket.icon = 'el-icon-circle-plus'
    add_ticket.type = 'info'
    add_ticket.action_type = 0
    add_ticket.action_url = '/courier/ticket/submit_ticket.html'

    def ticket_state(self, obj):
        if obj.active_type == 0:
            color_code = 'black'
            assign_state_name = '等待处理'
        elif obj.active_type == 1:
            color_code = '#409eff'
            assign_state_name = '进行中'
        elif obj.active_type == 2:
            color_code = '#67C23A'
            assign_state_name = '完成'
        elif obj.active_type == 3:
            color_code = '#F56C6C'
            assign_state_name = '驳回'
        else:
            color_code = 'yellow'
            assign_state_name = '未知'
        return format_html(
            '<a class="btn btn-xs btn-danger" style="display:inline-block;width:100px;text-align:center;padding:6px 0px;border-radius:4px;color: #fff;background: {};border-color: #1890ff;">{}</a>'.format(
                color_code,
                assign_state_name
            )
        )
    ticket_state.short_description = '状态'

    def handle_confirm(self, request, queryset):
        # 工单处理
        post = request.POST
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })
        if not request.user.is_superuser:
            return JsonResponse(data={
                'status': 'error',
                'msg': '没有权限处理！'
            })

        for handle_obj in queryset:
            change_active_type = int(post.get('type'))
            if change_active_type == 2 or change_active_type == 3:
                handle_obj.close_time = datetime.datetime.now()
                if not handle_obj.handle_time:
                    handle_obj.handle_time = datetime.datetime.now()
                handle_obj.time_consuming = (
                    handle_obj.close_time -
                    handle_obj.create_time).seconds  # 统计工单处理时长, 此处开始时间按照工单创建时间来算
            if change_active_type == 1:
                handle_obj.handle_time = datetime.datetime.now()
            handle_obj.op_id = request.user.username
            handle_obj.active_type = change_active_type
            handle_obj.handle_result = post.get('mask')
            handle_obj.save()
        return JsonResponse(data={
            'status': 'success',
            'msg': '处理成功！'
        })

    handle_confirm.short_description = '处理工单'
    handle_confirm.type = 'success'
    handle_confirm.icon = 'el-icon-s-promotion'
    # # 指定为弹出层，这个参数最关键
    handle_confirm.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '弹出层输入框',
        # 提示信息
        'tips': '请选择任务工单任务状态',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [{
            'type': 'select',
            'key': 'type',
            'label': '类型',
            'width': '200px',
            # size对应elementui的size，取值为：medium / small / mini
            'size': 'small',
            # value字段可以指定默认值
            'value': '1',
            'options': [{
                'key': '1',
                'label': '进行中'
            }, {
                'key': '2',
                'label': '完成'
            }, {
                'key': '3',
                'label': '驳回'
            },
            ]
        },
            {
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'textarea',
                # key 对应post参数中的key
                'key': 'mask',
                # 显示的文本
                'label': '备注',
                # 为空校验，默认为False
                'require': False,
                'width': '400px',

        },
        ]
    }

    def format_detail(self, obj):
        if len(obj.detail) > 3:
            return format_html('<pre>{}</pre>', obj.detail)
        else:
            return obj.detail
    format_detail.short_description = '工单详情'

    def save_model(self, request, obj, form, change):
        obj.create_by = request.user.username
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        ret = Ticket.objects.none()
        u_obj = User.objects.get(username=request.user.username)
        ret = ret | qs.filter(create_by=u_obj)
        return ret

    def has_delete_permission(self, request, obj=None):
        # qs = super().has_delete_permission(request)
        # if request.user.is_superuser:
        #     return qs
        pass

    def has_add_permission(self, request):
        pass

    # def delete_queryset(self, request, queryset):
    #     pass
    #
    # def delete_view(self, request, object_id, extra_context=None):
    #     pass
    #
    # def delete_model(self, request, obj):
    #     pass
