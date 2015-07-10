from django.contrib.auth.models import User
from django.db import models
from streaming import pubnub

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

class Player(User):
    server = models.CharField(choices=[(c, c) for c in SERVERS], max_length=25)
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
        pubnub.publish(
            channel=self.server,
            message='{p.username}'.format(p=self)
        )

    def delete(self, *args, **kwargs):
        super(Player, self).delete(*args, **kwargs)
        pubnub.publish(
            channel='torqueue-notifications',
            message=UNQ_NOTICE.format(p=self)
        )



class Character(models.Model):
    player = models.ForeignKey(Player)
    name = models.CharField(max_length=25)
    server = models.CharField(choices=[(c, c) for c in SERVERS], max_length=25)
    adv_class = models.CharField(
        choices=[(c, c) for c in ADV_CLASSES],
        max_length=25
    )

    def __repr__(self):
        return '{s.name} - {s.server}'.format(s=self)
