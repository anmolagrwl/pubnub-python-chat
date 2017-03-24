from pubnub import Pubnub
import sys
import os

def main():
    chatroom = input("Please enter the name of chat room you want to enter: ")
    user_name = input("Please enter your name: ")
    print("Hello {}. Welcome to {} chatroom".format(user_name, chatroom))

    pn = Pubnub(publish_key="demo", subscribe_key="demo", ssl_on=False, uuid=user_name)

    channel = chatroom

    def _callback(message, channel):
        if message['user_name'] != user_name:
            print("\n{}: {}".format(message['user_name'], message['message']))
            print("{}: ".format(user_name))

    # def _presence_callback(message):
    #     print(message)
    #     if message['action'] == 'join':
    #         print("\n{} joined...".format(message['uuid']))
    #
    #     if message['action'] == 'leave':
    #         print("\n{} left...".format(message['uuid']))

    def _error(error):
        print(error)

    def _history_callback(message):
        for msg in message[0] :
            print("\n{}: {}".format(msg['user_name'], msg['message']))

    def _whosonline_callback(message):
        print("Following are online :")
        print("-------------")
        for msg in message['uuids'] :
            print(msg)

    def _howmanyonline_callback(message):
        print("\n{} online...".format(message['occupancy']))

    def get_input():
        message = input("{}: ".format(user_name))

        if str(message) in ['quit', 'QUIT', 'Quit', 'exit', 'Exit', 'EXIT']:
            print("Quitting...")
            pn.unsubscribe(channel=channel)
            sys.stdout.flush()
            os._exit(0)
        elif str(message) in ['whosonline', 'whoisonline']:
            pn.here_now(channel=channel, callback=_whosonline_callback, error=_error)
        elif str(message) in ['howmanyonline']:
            pn.here_now(channel=channel, callback=_howmanyonline_callback, error=_error)
        else:
            msg_object = dict(user_name=user_name, message=message)
            pn.publish(channel=channel, message=msg_object)

    pn.subscribe(channels=channel, callback=_callback)

    # presence_channel = "{}-pnpres".format(channel)
    # pn.subscribe(channels=presence_channel, callback=_presence_callback)

    pn.history(channel=channel, count=100, callback=_history_callback, error=_error)

    while True:
        get_input()


if __name__ == "__main__":
    main()
