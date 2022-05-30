from django.db import models
from django.contrib.auth.models import Group
import jsonfield


class TicketType(models.Model):
    class Meta:
        verbose_name_plural = 'ticket'
        verbose_name = 'ticket'
    type_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='工单类型')
    ticket_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='工单名称')
    desc = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='描述')
    handle_user = models.ManyToManyField(to=Group, verbose_name='选择处理人',  blank=False)
    status_code = (
        (0, '是'),
        (1, '否'),
    )
    is_auto = models.IntegerField(
        choices=status_code,
        null=False,
        blank=False,
        default=1,
        verbose_name='是否可自动化')
    helper = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name='帮助信息')
    extra_params = jsonfield.JSONField(verbose_name='扩展字段', max_length=4096, null=True, blank=True)


    def __str__(self):
        return self.type_name



class Ticket(models.Model):
    class Meta:
        verbose_name_plural = 'ticket'
        verbose_name = 'ticket'

    ticket_type = models.ForeignKey(
        to=TicketType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="工单类型")
    ticket_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='工单名称')
    app_code = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='APPCODE')
    status_code = (
        (0, '等待处理'),
        (1, '进行中'),
        (2, '完成'),
        (3, '驳回')
    )
    active_type = models.IntegerField(
        choices=status_code,
        null=True,
        blank=True,
        default=0,
        verbose_name='状态')
    qa_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='QA')
    op_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='OPS')
    create_by = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='创建人')
    is_auto = models.IntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name='是否可自动化')

    extra_params = jsonfield.JSONField(max_length=4096, null=True, blank=True, verbose_name='扩展表')
    detail = models.TextField(max_length=4096, null=True, blank=True, verbose_name='工单详情')
    handle_result = models.TextField(max_length=4096, null=True, blank=True, verbose_name='处理意见')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    close_time = models.DateTimeField(verbose_name="关闭时间", null=True, blank=True)
    handle_time = models.DateTimeField(verbose_name="处理时间", null=True, blank=True)
    time_consuming = models.IntegerField(null=True, blank=True, verbose_name='工单耗时')

    def __str__(self):
        return self.ticket_type.desc







