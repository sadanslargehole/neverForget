from tortoise.models import Model
from tortoise import fields
import discord


class guild(Model):
    id = fields.BigIntField(pk=True)
    canUseBot = fields.BooleanField()
    unpinChannel = fields.BigIntField()
    enabled = fields.BooleanField()
    whitelist = fields.BooleanField()
    whitelistedChannels = fields.BigIntField()
    blacklistedChannels = fields.BigIntField()
    blacklistedUsers = fields.BigIntField()

    def __str__(self):
        return f'{self.id} {self.canUseBot} {self.unpinChannel} {self.enabled} {self.whitelist} {self.whitelistedChannels} {self.blacklistedChannels} {self.blacklistedUsers}'


class user(Model):
    id = fields.BigIntField(pk=True)
    canUseBot = fields.BooleanField()
    watchForUnpins = fields.BooleanField()
    canAddToServer = fields.BooleanField()

    def __str__(self):
        return f'{self.id} {self.canUseBot} {self.watchForUnpins} {self.canAddToServer}'
