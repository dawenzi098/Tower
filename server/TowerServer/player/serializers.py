from rest_framework import serializers

from Tower.server.TowerServer.player.models import Player


class RegisterSrlz(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('',)
