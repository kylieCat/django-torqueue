from django.contrib.auth.models import User
from django.db import models
# from streaming import pubnub

Q_NOTICE = '{p.username} on Team: {p.team} has queued on {p.server}'
UNQ_NOTICE = '{p.username} on Team: {p.team} has left the queue on {p.server}'


SERVERS = (
    'The Bastion',
    'Bergeren Colony',
    'The Harbinger',
    'The Shadowlands',
    'Jung Ma',
    'The Ebon Hawk',
    'Prophecy of the Five',
    'Jedi Covenant',
)

ADV_CLASSES = (
    'Powertech',
    'Mercenary',
    'Vanguard',
    'Commando',
    'Sorcerer',
    'Assassin',
    'Sage',
    'Shadow',
    'Sniper',
    'Operative',
    'Gunslinger',
    'Scoundrel',
    'Juggernaut',
    'Marauder',
    'Guardian',
    'Sentinel'
)

class Server(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    def __iter__(self):
        for player in self.player_set.all():
            yield player


class Player(User):
    server = models.ForeignKey(Server)
    adv_class = models.CharField(
        choices=[(c, c) for c in ADV_CLASSES],
        max_length=25
    )
    team = models.CharField(max_length=50,blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Player, self).save(*args, **kwargs)
        pubnub.publish(
            channel='torqueue-notifications',
            message=Q_NOTICE.format(p=self)
        )

    def delete(self, *args, **kwargs):
        super(Player, self).delete(*args, **kwargs)
        pubnub.publish(
            channel='torqueue-notifications',
            message=UNQ_NOTICE.format(p=self)
        )

    def __str__(self):
        return '<{p.username} - {p.team}>'.format(p=self)


# This code will be used at a later date
# class Character(models.Model):
#     player = models.ForeignKey(Player)
#     name = models.CharField(max_length=25)
#     server = models.CharField(choices=[(c, c) for c in SERVERS], max_length=25)
#     adv_class = models.CharField(
#         choices=[(c, c) for c in ADV_CLASSES],
#         max_length=25
#     )
#
#     def __repr__(self):
#         return '{s.name} - {s.server}'.format(s=self)
