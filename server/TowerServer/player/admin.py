from django.contrib import admin

# Register your models here.
from player.models import Player, TowerPlayer, Tower


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'coin', 'post_date')


class TowerAdmin(admin.ModelAdmin):
    list_display = ('player', 'post_date')


class TowerPlayerAdmin(admin.ModelAdmin):
    list_display = ('player', 'level', 'hp', 'atk', 'defense')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Tower, TowerAdmin)
admin.site.register(TowerPlayer, TowerPlayerAdmin)
