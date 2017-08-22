from __future__ import absolute_import

from celery import shared_task
from celery.schedules import crontab
import logging
from api.models import Inbox, Outbox
from django.conf import settings
import time
from multiprocessing.dummy import Pool as ThreadPool
import random
from django.core.cache import cache
import requests



logger = logging.getLogger(__name__)

timeout = 10
unprocessed = 0
pool_size = 10
channel = 3 #ToDo, check
channel_uuid = 'b3dca918-d797-48a0-b1ff-b3a7b963c4b6'
pending = 2

@shared_task
def rapidpro_pusher():
    start = time.time()
    print 'Starting....'
    #logger.info('*'*10)
    #logger.info(settings.RAPIDPRO_ENDPOINT)
    messages = Inbox.objects.filter(processed=unprocessed)
    if messages:
        logger.info('Found %d unprocessed messages'  % len(messages))
        #Create processing thread for each message
        push_to_rapidpro(messages)
        print '%s unprocessed messages ' % len(messages)
    else:
        print 'No inbound messages'

    print 'Done.....{}s'.format( time.time() - start)
    #time.sleep(random.randint(5, 10))


def push_to_rapidpro(messages):
    logger.info("Pushing {} messages".format(len(messages)))
    # Make the Pool of workers
    pool = ThreadPool(pool_size)
    # Opens each message with its own thread
    # and return the results
    results = pool.map_async(push, messages)
    #close the pool and wait for the work to finish
    pool.close()
    pool.join()


def push(message):
    logger.info('.....')
    logger.info('Pushing to RP :Sender={}'.format(message.sender))

    #trigger flow on keyworkds
    if message.body in settings.RAPIDPRO_FLOWTRIGGER_KEYWORDS:
        #Trigger flow
        logger.info('************ Initialize and trigger flow *****************')
        initialize_and_trigger_flow(message)

    else:
        #Check if user is on a flow and push a message
        if cache.get(message.sender):
            txt_message = {
                'from': message.sender,
                'text': message.body,
                'channel': channel,
                'id': 309
            }
            logger.info('Running post_received() ....')
            post_received(txt_message)

            #remember this as last message sent
            sender_cache = {} if not cache.get(message.sender) else cache.get(message.sender)
            sender_cache['last_message'] = message.id

            cache.set(message.sender, sender_cache)

            message.processed = pending
            message.save()
            #time.sleep(random.randint(1,5))
            logger.info('Done pushing message to {}...'.format(message.sender))
        else:
            #Trigger flow
            initialize_and_trigger_flow(message)
            logger.info('Done triggering new flow....')
            #time.sleep(random.randint(5,10))


def initialize_and_trigger_flow(message):
    try:
        flow_uuid = settings.CATEGORY_FLOW_MAP[message.category]
    except KeyError as e:
        logger.error(e)
        logger.error('SMS Category %s has no flow mapping. Please check CATEGORY_FLOW_MAP setting')
        return

    details = {
      "flow": flow_uuid,
      "urns": ["tel:{}".format(message.sender)],
      "extras": {
        "campaign": "Pharmacy Council"
      },
      "restart_participants": 1
    }
    logger.info('Triggering new flow ....')
    contacts = trigger_rp_flow(details)

    #set user-flow cache
    cache.set(message.sender, {
        'flow': flow_uuid
    })

    message.processed = pending
    message.save()


def trigger_rp_flow(details):
    #Flow trigger URL = http://localhost:8002/api/v2/flow_starts.json
    flow_trigger_endpoint = '{}/api/v2/flow_starts.json'.format(settings.RAPIDPRO_ENDPOINT)
    headers = {
        'Authorization': 'Token {}'.format(settings.RAPIDPRO_API_TOKEN)
        }
    result = requests.post(flow_trigger_endpoint, data=details, headers=headers)
    json_response = result.json()
    if result.status_code in (200,201,):
        print json_response
        return json_response['contacts']

    print 'Error:{}'.format(json_response)
    return



def post_received(message):
    #SMS push URL =  http://localhost:8002/handlers/external/received/450908e9-3d32-448f-bfa8-66d177e21afd/
    sms_push_endpoint = '{}/handlers/external/received/{}/'.format(settings.RAPIDPRO_ENDPOINT, channel_uuid)
    headers = {
        'Authorization': 'Token {}'.format(settings.RAPIDPRO_API_TOKEN)
    }
    result = requests.post(sms_push_endpoint, data=message, headers=headers)
    logger.info('{} returned {}'.format(sms_push_endpoint, result.text))

    if result.status_code == 200:
        if 'Accepted' in result.text:
            return 200
    return
