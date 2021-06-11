#!/usr/bin/env python3
"""
This file contains the requestor part of our application. There are three areas here:
1. Splitting the data into multiple tasks, each of which can be executed by a provider.
2. Defining what commands must be run within the provider's VM.
3. Scheduling the tasks via a yagna node running locally.
"""

import argparse
import asyncio
from datetime import timedelta
from pathlib import Path
from typing import AsyncIterable, Iterator

from yapapi import Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm

import worker

# CLI arguments definition
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--hash", type=Path, default=Path("data/hash.json"))
arg_parser.add_argument("--subnet", type=str, default="devnet-beta.2")
arg_parser.add_argument("--words", type=Path, default=Path("data/words.txt"))

# Container object for parsed arguments
args = argparse.Namespace()

ENTRYPOINT_PATH = Path("/golem/entrypoint/worker.py")
TASK_TIMEOUT = timedelta(minutes=10)

def data(words_file: Path, chunk_size: int = 100_000) -> Iterator[Task]:
    """Split input data into chunks, each one being a single `Task` object.

    A single provider may compute multiple tasks.
    Return an iterator of `Task` objects.
    """
    # TODO

async def steps(context: WorkContext, tasks: AsyncIterable[Task]):
    """Prepare a sequence of steps which need to happen for a task to be computed.

    `WorkContext` is a utility which allows us to define a series of commands to
    interact with a provider.
    Tasks are provided from a common, asynchronous queue.
    The signature of this function cannot change, as it's used internally by `Executor`.
    """
    # TODO

async def main():
    # Set of parameters for the VM run by each of the providers
    package = await vm.repo(
        image_hash="1e53d1f82b4c49b111196fcb4653fce31face122a174d9c60d06cf9a",
        min_mem_gib=1.0,
        min_storage_gib=2.0,
    )

    # TODO Run Executor using data and steps functions

if __name__ == "__main__":
    args = arg_parser.parse_args()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    # yapapi debug logging to a file
    enable_default_logger(log_file="yapapi.log")

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        # Make sure Executor is closed gracefully before exiting
        task.cancel()
        loop.run_until_complete(task)
