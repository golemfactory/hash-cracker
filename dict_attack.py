#!/usr/bin/env python3

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
from yapapi.rest.activity import BatchTimeoutError


def data(dict_file: Path, chunk_count: int) -> Iterator[Task]:
    with dict_file.open() as f:
        lines = [line.strip() for line in f]

    chunk_size = math.ceil(len(lines) / chunk_count)

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i : i + chunk_size]
        yield Task(data=chunk)


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        data = task.data

        script_dir = Path(__file__).resolve().parent
        hash_path = str(script_dir / "hash.json")

        context.send_json("/golem/input/params.json", task.data)
        context.send_file(hash_path, "/golem/input/hash.json")

        context.run("/golem/entrypoint/worker.py")

        output_file = NamedTemporaryFile()
        context.download_file("/golem/output/result.json", output_file.name)

        try:
            yield context.commit(timeout=timedelta(seconds=120))
            task.accept_result(result=json.load(output_file))
            output_file.close()
        except BatchTimeoutError:
            print(f"task timed out: {context.provider_name}, {task.running_time}")
            raise


async def main():
    package = await vm.repo(
        image_hash="431ed2a12725a7341e8332a4e223bb54c45babc7bedbf3896956ea7c",
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )

    executor = Executor(
        package=package,
        budget=1,
        subnet_tag="goth",
        event_consumer=log_summary(log_event_repr),
        timeout=timedelta(minutes=10),
    )

    result = ""
    async with executor:
        async for task in executor.submit(worker, data(Path("dict.txt"), 2)):
            print(
                f"task computed: {task}, result: {task.result}, time: {task.running_time}"
            )

            if task.result:
                result = task.result

        if result:
            print(f'Found matching word: {result}')
        else:
            print('No matching words found.')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    enable_default_logger(
        log_file="yapapi.log",
        debug_activity_api=True,
        debug_market_api=True,
        debug_payment_api=True,
    )

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
