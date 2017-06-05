"""Slack Monitor to Ansible Build Command Bridge."""
from __future__ import print_function

import os
import socket
import time

from slackclient import SlackClient
import delegator

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

try:
    SillyError = BrokenPipeError  # pylint: disable=invalid-name
except NameError:
    SillyError = socket.error  # pylint: disable=invalid-name

# pip install slackclient delegator.py python-dotenv

# [{
#    'channel': 'C5LALU1JS',
#    'subtype': 'bot_message',
#    'type': 'message',
#    'attachments': [{
#        'color': '36a64f',
#        'fallback': 'Build <https://travis-ci.org/ScorpionResponse/freelancefinder/builds/239304550?utm_source=slack&utm_medium=notification|#764> (<https://github.com/ScorpionResponse/freelancefinder/compare/ee6442dfe32a...b55b24ddb72b|b55b24d>) of ScorpionResponse/freelancefinder@develop by Paul Moss passed in 13 min 33 sec'
#            ,
#        'id': 1,
#        'text': 'Build
#        <https://travis-ci.org/ScorpionResponse/freelancefinder/builds/239304550?utm_source=slack&utm_medium=notification|#764>
#        (<https://github.com/ScorpionResponse/freelancefinder/compare/ee6442dfe32a...b55b24ddb72b|b55b24d>)
#        of ScorpionResponse/freelancefinder@develop by Paul Moss passed in 13
#        min 33 sec'
#            ,
#        }],
#    'event_ts': '1496584116.638861',
#    'bot_id': 'B5JS3UKA4',
#    'team': 'T5KHSKJCU',
#    'text': '',
#    'ts': '1496584116.638861',
#    }]


def deploy_develop():
    """Deploy the development version of the software."""
    result = delegator.run('cd ~/freelancefinder/ansible; make webservers', block=True)
    return result


def deploy_production():
    """Deploy the production version of the software."""
    result = delegator.run('cd ~/freelancefinder/ansible; make webservers-prod', block=True)
    return result


def parse_build_message(build_message):
    """Get info out of the travis build message."""
    build_num = 'unknown'
    build_id = 'unknown'
    branch = 'unknown'
    status = 'unknown'

    # TODO(Paul): OMG hax.  This will break probably.
    words = build_message.split(' ')
    for word in words:
        if word.startswith('<') and word.endswith('>'):
            build_num = word
        if word.startswith('(') and word.endswith(')'):
            build_id = word[1:-1]
        if word.startswith('ScorpionResponse/freelancefinder@'):
            branch = word.split('@')[1]
        if word in ('passed', 'failed'):
            status = word
    return branch, status, build_num, build_id


def post_to_channel(slack_client, message, thread_ts):
    """Post a message to the slack channel."""
    print("Sending message: {}".format(message))
    slack_client.api_call(
        "chat.postMessage",
        channel="#builds",
        text=message,
        thread_ts=thread_ts,
        reply_broadcast=True
    )


def respond_to_build(slack_client, branch, build_num, build_id, thread_ts):
    """Take action on successful build results."""
    if branch == 'develop':
        result = deploy_develop()
    elif branch == 'master':
        message = "Build {} - {}/{} production deployment started".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts)
        result = deploy_production()
    else:
        # Do nothing
        return None
    if result.return_code == 0:
        message = "Build {} - {}/{} successfully deployed".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts)
    else:
        message = "FAILED: Build {} - {}/{} failed to deploy.".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts)
        print(result.err)


def main():
    """Run client."""
    slack_token = os.environ["SLACK_API_TOKEN"]
    slack_client = SlackClient(slack_token)

    if not slack_client.rtm_connect():
        print("Connection Failed, invalid token?")

    seen_error = False
    while True:
        try:
            current_messages = slack_client.rtm_read()
            for mess in current_messages:
                if 'bot_id' in mess and mess['bot_id'] == 'B5JS3UKA4':
                    build_message = mess['attachments'][0]['text']
                    print("Got Build Message: {build_message}".format(build_message=build_message))
                    branch, status, build_num, build_id = parse_build_message(build_message)
                    if status == 'passed':
                        respond_to_build(slack_client, branch, build_num, build_id, mess['ts'])
            time.sleep(30)
        except SillyError:
            print("Got BrokenPipeError.")
            if seen_error:
                raise
            seen_error = True
            time.sleep(30)
            slack_client.rtm_connect()
        except Exception as exp:  # pylint: disable=broad-except
            print("Got some other error: {}".format(exp))
            if seen_error:
                raise
            seen_error = True
            time.sleep(30)
            slack_client.rtm_connect()


if __name__ == '__main__':
    main()
