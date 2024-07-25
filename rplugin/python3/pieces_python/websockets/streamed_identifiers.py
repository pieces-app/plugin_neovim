"""
A class for caching Streamed Identifiers. This class is designed to be inherited.

Attributes:
    identifiers_snapshot (Dict[str, Union[Asset, Conversation]]): A dictionary mapping IDs to their corresponding API call results.
    identifiers_queue (queue.Queue): A queue for IDs to be processed.
    identifiers_set (set): A set for IDs currently in the queue.
    api_call (Callable[[str], Union[Asset, Conversation]]): A callable that takes an ID and returns either an Asset or a Conversation.
    block (bool): A flag to indicate whether to wait for the queue to receive the first ID.
    first_shot (bool): A flag to indicate if it's the first time to open the websocket.
    lock (threading.Lock): A lock for thread safety.
    worker_thread (threading.Thread): A thread for processing the queue.

Methods:
    worker(): Continuously processes IDs from the queue and updates the identifiers_snapshot.
    update_identifier(id: str): Updates the identifier snapshot with the result of the API call.
    streamed_identifiers_callback(ids: StreamedIdentifiers): Callback method to handle streamed identifiers.

Example:
    class AssetSnapshot(StreamedIdentifiersCache,api_call=AssetApi(PiecesSettings.api_client).asset_snapshot):
        pass
"""

import queue
import threading
from typing import Dict, Union, Callable
from .._pieces_lib.pieces_os_client import Conversation, StreamedIdentifiers, Asset
from abc import ABC,abstractmethod


class StreamedIdentifiersCache(ABC):
    """
    This class is made for caching Streamed Identifiers.
    Please use this class only as a parent class.
    """

    def __init_subclass__(cls, api_call: Callable[[str], Union[Asset, Conversation]], **kwargs):
        super().__init_subclass__(**kwargs)
        cls.identifiers_snapshot: Dict[str, Union[Asset, Conversation,None]] = {}  # Map id:return from the api_call
        cls.identifiers_queue = queue.Queue()  # Queue for ids to be processed
        cls.identifiers_set = set()  # Set for ids in the queue
        cls.api_call = api_call
        cls.block = True  # to wait for the queue to receive the first id
        cls.first_shot = True  # First time to open the websocket or not


    @abstractmethod
    def sort_first_shot():
        """
            Sorting algrothim in the first shot
        """
        pass

    @classmethod
    def worker(cls):
        while True:
            
            try:
                id = cls.identifiers_queue.get(block=cls.block, timeout=5)
                if id in cls.identifiers_set:
                    cls.identifiers_set.remove(id)  # Remove the id from the set
                    cls.update_identifier(id)
                    cls.identifiers_queue.task_done()
            except queue.Empty:  # queue is empty and the block is false
                if cls.block:
                    continue  # if there are more ids to load

                if cls.first_shot:
                    cls.first_shot = False
                    cls.sort_first_shot()

                return  # End the worker

    @classmethod
    def update_identifier(cls, identifier: str):
        try:
            id_value = cls.api_call(identifier)
            cls.identifiers_snapshot[identifier] = id_value
            return id_value
        except:
            return None

    @classmethod
    def streamed_identifiers_callback(cls, ids: StreamedIdentifiers):
        # Start the worker thread if it's not running
        cls.block = True
        thread = threading.Thread(target=cls.worker)
        thread.start()
        for item in ids.iterable:
            reference_id = item.asset.id if item.asset else item.conversation.id  # Get either the conversation or the asset

            if reference_id not in cls.identifiers_set:
                if item.deleted:
                    # Asset deleted
                    cls.identifiers_snapshot.pop(reference_id, None)
                else:
                    if reference_id not in cls.identifiers_snapshot and not cls.first_shot:
                        cls.identifiers_snapshot = {reference_id: None, **cls.identifiers_snapshot}
                    cls.identifiers_queue.put(reference_id)  # Add id to the queue
                    cls.identifiers_set.add(reference_id)  # Add id to the set

        cls.block = False  # Remove the block to end the thread
