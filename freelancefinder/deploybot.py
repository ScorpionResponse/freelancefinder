"""Slack Monitor to Ansible Build Command Bridge."""
from __future__ import print_function

import logging
import os
import sys
import time

from slackclient import SlackClient
import delegator

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logging.basicConfig(filename='build.log', level=logging.DEBUG)

THIS_BOT_ID = "U5MR114V7"
TRAVIS_BOT_ID = "B5JS3UKA4"

ERROR_THRESHOLD = 10

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


def post_to_channel(slack_client, message, thread_ts, announce=True):
    """Post a message to the slack channel."""
    logging.info("Sending message: %s", message)
    slack_client.api_call(
        "chat.postMessage",
        channel="#builds",
        text=message,
        thread_ts=thread_ts,
        reply_broadcast=announce
    )


def respond_to_build(slack_client, branch, build_num, build_id, thread_ts):
    """Take action on successful build results."""
    logging.debug("Responding to build: Branch-%s; BuildNum-%s; BuildID-%s; ThreadID-%s", branch, build_num, build_id, thread_ts)
    is_production = False
    if branch == 'develop':
        message = "Build {} - {}/{} development deployment started".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
        result = deploy_develop()
    elif branch == 'master':
        is_production = True
        message = "Build {} - {}/{} production deployment started".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
        result = deploy_production()
    else:
        # Do nothing
        return None
    if result.return_code == 0:
        message = "Build {} - {}/{} successfully deployed".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
    else:
        message = "FAILED: Build {} - {}/{} failed to deploy.".format(build_num, branch, build_id)
        post_to_channel(slack_client, message, thread_ts)
        logging.debug("Failed build stdout: %s", result.out)
        logging.debug("Failed build stderr: %s", result.err)


def respond_to_command(slack_client, branch, thread_ts):
    """Take action on command."""
    logging.debug("Responding to command: Deploy Branch-%s", branch)
    is_production = False
    if branch == 'develop':
        message = "Development deployment started"
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
        result = deploy_develop()
    elif branch == 'master':
        is_production = True
        message = "Production deployment started"
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
        result = deploy_production()
    else:
        # Do nothing
        return None
    if result.return_code == 0:
        message = "Branch {} deployed successfully.".format(branch)
        post_to_channel(slack_client, message, thread_ts, announce=is_production)
    else:
        message = "FAILED: Branch {} failed to deploy.".format(branch)
        post_to_channel(slack_client, message, thread_ts)
        logging.debug("Failed build stdout: %s", result.out)
        logging.debug("Failed build stderr: %s", result.err)


def main():
    """Run client."""
    slack_token = os.environ["SLACK_API_TOKEN"]
    slack_client = SlackClient(slack_token)

    if not slack_client.rtm_connect():
        logging.error("Connection Failed, invalid token?")

    seen_error = 0
    while True:
        try:
            current_messages = slack_client.rtm_read()
            for mess in current_messages:
                logging.debug("Got Message: %s", mess)
                if mess['type'] == 'message' and 'bot_id' in mess and mess['bot_id'] == TRAVIS_BOT_ID:
                    build_message = mess['attachments'][0]['text']
                    logging.info("Got Build Message: %s", build_message)
                    branch, status, build_num, build_id = parse_build_message(build_message)
                    if status == 'passed':
                        respond_to_build(slack_client, branch, build_num, build_id, mess['ts'])
                elif mess['type'] == 'message' and 'text' in mess and mess['text'].startswith('<@{}>'.format(THIS_BOT_ID)):
                    words = mess['text'].split(' ')
                    if words[1] == 'deploy' and words[2] in ('develop', 'master'):
                        respond_to_command(slack_client, words[2], mess['ts'])
            time.sleep(1)
        except Exception as exp:  # pylint: disable=broad-except
            seen_error += 1
            logging.error("Error count: %s - Error: %s", seen_error, exp)
            if seen_error > ERROR_THRESHOLD:
                raise
            time.sleep(30)
            slack_client.rtm_connect()
        sys.stdout.flush()


if __name__ == '__main__':
    main()
