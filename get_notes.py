import json 
import ssl
import time
import logging
import os
from dotenv import load_dotenv
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey
from datetime import datetime, timedelta


load_dotenv()

def get_notes(feed_type):
    events = []
    if feed_type:
        nsec = os.getenv(f"NOSTR_NSEC_{feed_type}", "Missing env variable")
        priv_key = PrivateKey.from_nsec(nsec)
        pub_key = priv_key.public_key.hex()

    # Get the current date and time
    current_date = datetime.now()

    # Calculate the date two days ago
    two_days_ago = current_date - timedelta(days=2)
    unix_time_two_days_ago = int(two_days_ago.timestamp())
    filters = Filters([Filter(authors=[pub_key], kinds=[EventKind.TEXT_NOTE], since=unix_time_two_days_ago)])
    subscription_id = "guRawRYpzgwwTaFj3iCCbiTEhGHgsPtr"
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://nos.lol")
    relay_manager.add_relay("wss://relay.snort.social")
    relay_manager.add_relay("wss://relay.current.fyi")
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    message = json.dumps(request)
    relay_manager.publish_message(message)
    time.sleep(1) # allow the messages to send

    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        events.append(event_msg.event.content)
    
    relay_manager.close_connections()
    return(events)