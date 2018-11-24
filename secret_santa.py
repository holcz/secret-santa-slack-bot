import os
from random import shuffle

from slackclient import SlackClient

class Member(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

def pairing(members_list):
    shuffled_list = list(members_list)
    shuffled_list = every_day_im_shuffling(members_list, shuffled_list)
    pair_map = {}
    
    for i in xrange(0, len(members_list)):
        pair_map[members_list[i].id] = shuffled_list[i]
    
    return pair_map

def every_day_im_shuffling(members_list, shuffled_list):
    print "Shuffling"
    shuffle(shuffled_list)
    paring_good = True
    for i in xrange(0, len(members_list)):
        if members_list[i].id == shuffled_list[i].id:
            paring_good = False
            break
    if paring_good:
        return shuffled_list
    return every_day_im_shuffling(members_list, shuffled_list)

slack_token = os.environ["SLACK_API_TOKEN"]
is_dry_run = os.environ.get("DRY_RUN", False)
secret_santa_channel_name = os.environ.get("CHANNEL_NAME", "secret-santa")

sc = SlackClient(slack_token)

channels = sc.api_call("channels.list")['channels']
all_members = sc.api_call("users.list")['members']

secret_santa_channel = [channel for channel in channels if channel['name'] == secret_santa_channel_name][0]
secret_santa_channel_info = sc.api_call("channels.info", channel=secret_santa_channel['id'])['channel']

secret_santa_member_ids = set(secret_santa_channel_info['members'])

secret_santa_members = [Member(member['id'], member['real_name']) for member in all_members if member['id'] in secret_santa_member_ids]

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
        message = "Ho Ho Ho. You were assigned to: {}\nBe sure you make her/him Happy!\nMerry Christmas! :santa:".format(
            pairing_map[user_id].name
        )
        sc.api_call("chat.postMessage",
            channel=direct_message_channels[user_id],
            text=message,
            as_user=False,
            icon_emoji=":santa:"
        )

print "Ho ho ho, everyone will be Happy!"
