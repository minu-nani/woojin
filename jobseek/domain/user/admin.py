# Register your models here.
from django.contrib import admin

from jobseek.domain.user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile_id', 'user', 'user_id', 'masked_name', 'masked_tel_num', 'birthday',)
    search_fields = ('masked_name', 'masked_tel_num', 'user_profile_id', 'user__id',)
    readonly_fields = ('modified_at',)


admin.site.register(UserProfile, UserProfileAdmin)
