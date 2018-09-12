from rest_framework import serializers

from player.models import Player


class PlayerSrlz(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('nickname', 'hp', 'atk', 'defense', 'coin')
