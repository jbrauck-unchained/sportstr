import json 
import ssl
import time
import logging
import os
from dotenv import load_dotenv
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey

logging.basicConfig(level=logging.INFO)

load_dotenv()

def post_note(headline, feed_type):
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://nos.lol")
    relay_manager.add_relay("wss://relay.snort.social")
    relay_manager.add_relay("wss://relay.current.fyi")
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open
    if feed_type:
        nsec = os.getenv(f"NOSTR_NSEC_{feed_type}", "Missing env variable")
        priv_key = PrivateKey.from_nsec(nsec)
        pub_key = priv_key.public_key.hex()
    else:
        logging.error("Feed type not provided.")
        return

    event = Event(content=headline, public_key=pub_key)
    priv_key.sign_event(event)

    output = relay_manager.publish_event(event)
    print(output)
    time.sleep(1) # allow the messages to send
    logging.info(f"Published event: {headline}")

    relay_manager.close_connections()