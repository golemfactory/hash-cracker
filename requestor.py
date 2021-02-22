#!/usr/bin/env python3

import argparse
import asyncio
from datetime import timedelta
import json
import math
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import AsyncIterable, Iterator

from yapapi import Executor, Task, WorkContext
from yapapi.log import enable_default_logger, log_event_repr, log_summary
from yapapi.package import vm

from worker import HASH_PATH, WORDS_PATH, RESULT_PATH

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--hash", type=Path, default=Path("hash.json"))
arg_parser.add_argument("--words", type=Path, default=Path("words-short.txt"))
arg_parser.add_argument("--workers", type=Path, default=2)

args = argparse.Namespace()

TASK_TIMEOUT = timedelta(minutes=10)
WORKER_TIMEOUT = timedelta(seconds=120)


def data(dict_file: Path, chunk_count: int) -> Iterator[Task]:
    with dict_file.open() as f:
        lines = [line.strip() for line in f]

    chunk_size = math.ceil(len(lines) / chunk_count)

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        yield Task(data=chunk)


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        context.send_json(str(WORDS_PATH), task.data)
        context.send_file(str(args.hash), str(HASH_PATH))

        context.run("/golem/entrypoint/worker.py")

        output_file = NamedTemporaryFile()
        context.download_file(str(RESULT_PATH), output_file.name)

        yield context.commit(timeout=WORKER_TIMEOUT)
        task.accept_result(result=json.load(output_file))
        output_file.close()


async def main():
    package = await vm.repo(
        image_hash="1e53d1f82b4c49b111196fcb4653fce31face122a174d9c60d06cf9a",
        min_mem_gib=1.0,
        min_storage_gib=2.0,
    )

    executor = Executor(
        package=package,
        budget=1,
        subnet_tag="goth",
        event_consumer=log_summary(log_event_repr),
        timeout=TASK_TIMEOUT,
    )

    result = ""
    async with executor:
        data_iterator = data(args.words, args.workers)
        async for task in executor.submit(worker, data_iterator):
            print(f"task computed: {task}, result: {task.result}")

            if task.result:
                result = task.result

        if result:
            print(f"Found matching word: {result}")
        else:
            print("No matching words found.")


if __name__ == "__main__":
    args = arg_parser.parse_args()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    enable_default_logger()

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
