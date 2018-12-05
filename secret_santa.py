import os
from random import shuffle

from slackclient import SlackClient

class Member(object):
    def __init__(self, id, name, real_name):
        self.id = id
        self.name = name
        self.real_name = real_name

def pairing(members_list):
    shuffled_list = list(members_list)
    shuffle(shuffled_list)
    pair_map = {shuffled_list[i-1].id: shuffled_list[i] for i in xrange(1, len(shuffled_list))}
    pair_map[shuffled_list[len(shuffled_list)-1].id] = shuffled_list[0]
    return pair_map

slack_token = os.environ["SLACK_API_TOKEN"]
is_dry_run = os.environ.get("DRY_RUN", False)
secret_santa_channel_name = os.environ.get("CHANNEL_NAME", "secret-santa")

sc = SlackClient(slack_token)

channels = sc.api_call("channels.list")['channels']
all_members = sc.api_call("users.list")['members']

secret_santa_channel = [channel for channel in channels if channel['name'] == secret_santa_channel_name][0]
secret_santa_channel_info = sc.api_call("channels.info", channel=secret_santa_channel['id'])['channel']

secret_santa_member_ids = set(secret_santa_channel_info['members'])

secret_santa_members = [Member(member['id'], member['name'], member['real_name']) for member in all_members if member['id'] in secret_santa_member_ids]

pairing_map = pairing(secret_santa_members)

direct_message_channels = {}
for user_id in pairing_map:
    direct_message_channel = sc.api_call("im.open", user=user_id)
    if direct_message_channel.get("ok"):
        direct_message_channels[user_id] = direct_message_channel['channel']['id']
    else:
        print "Failed to open direct message to: {}".format(user_id)

if len(direct_message_channels) != len(pairing_map):
    print "Failed: No message was sent. See above!"
    exit

for user_id in pairing_map:
    if (is_dry_run):
        print "{} : {}".format(user_id, pairing_map[user_id].id)
    else:
        message = "Ho Ho Ho. You were assigned to: <@{username}>!\nHoliday cheer is in the air, and {real_name}'s happyness is in your hands!\nMerry Christmas! :christmas_tree:".format(
            real_name=pairing_map[user_id].real_name,
            username=pairing_map[user_id].name,
        )
        sc.api_call("chat.postMessage",
            channel=direct_message_channels[user_id],
            text=message,
            as_user=False,
            icon_url="https://avatars.slack-edge.com/2018-12-05/495885983556_b649926cc18291205483_48.png",
            username="Secret Santa"
        )

print "Ho ho ho, everyone will be Happy!"
