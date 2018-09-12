from django.contrib import admin

# Register your models here.
from player.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'coin', 'post_date')


admin.site.register(Player, PlayerAdmin)
