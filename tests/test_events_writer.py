import asyncio
import unittest
from asyncio.exceptions import CancelledError
from typing import cast
from datetime import datetime

from amberflo.blob_client import BlobWriter
from amberflo.events_writer import AsyncEventsWriter
from amberflo.utils import make_key
from amberflo.events_buffer import EventsBuffer


class DummyWriter(BlobWriter):
    def __init__(self):
        self.items = []

    async def put_object(self, key: str, body: bytes) -> None:
        self.items.append((key, body))

    def make_key(self, timestamp: datetime) -> str:
        return make_key(timestamp, "path")


class TestEventsWriter(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_events_are_written_when_batch_size_is_reached(self):
        dummy = DummyWriter()
        unit = AsyncEventsWriter(dummy, EventsBuffer(), batch_size=3)

        self.loop.run_until_complete(unit.async_write([{}]))

        self.assertEqual(len(dummy.items), 0)

        self.loop.run_until_complete(unit.async_write([{}]))

        self.assertEqual(len(dummy.items), 0)

        self.loop.run_until_complete(unit.async_write([{}]))

        self.assertEqual(len(dummy.items), 1)

    def test_events_are_written_when_periodic_flushing_runs(self):
        dummy = DummyWriter()
        unit = AsyncEventsWriter(dummy, EventsBuffer(), flush_interval=1, batch_size=3)

        self.loop.run_until_complete(unit.async_write([{}]))

        self.assertEqual(len(dummy.items), 0)

        self.loop.run_until_complete(asyncio.sleep(1))

        self.assertEqual(len(dummy.items), 1)

    def test_events_are_written_when_periodic_flushing_is_cancelled(self):
        dummy = DummyWriter()
        unit = AsyncEventsWriter(dummy, EventsBuffer())

        self.loop.run_until_complete(unit.async_write([{}]))

        self.assertEqual(len(dummy.items), 0)

        # satisfy type checking
        task = cast(asyncio.Task, unit.flush_task)

        task.cancel()

        with self.assertRaises(CancelledError):
            self.loop.run_until_complete(task)

        self.assertEqual(len(dummy.items), 1)

    def test_no_events_are_written_if_none_is_recorded(self):
        dummy = DummyWriter()
        unit = AsyncEventsWriter(dummy, EventsBuffer())

        self.loop.run_until_complete(unit.async_write([]))

        self.assertEqual(len(dummy.items), 0)

        # satisfy type checking
        task = cast(asyncio.Task, unit.flush_task)

        task.cancel()

        with self.assertRaises(CancelledError):
            self.loop.run_until_complete(task)

        self.assertEqual(len(dummy.items), 0)
