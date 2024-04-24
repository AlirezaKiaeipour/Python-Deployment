import time 
import random
import asyncio

async def download_file():
    print("Download File Started")
    random_execution_time = random.randint(0,8)
    await asyncio.sleep(random_execution_time)
    print("Download File Ended")


async def extract_file():
    print("Extract File Started")
    random_execution_time = random.randint(0,8)
    await asyncio.sleep(random_execution_time)


async def download():
    print("Download Started")
    await download_file()
    await extract_file()
    print("Download Ended")


async def video_process():
    print("Create Video Started")
    random_execution_time = random.randint(0,8)
    await asyncio.sleep(random_execution_time)
    print("Create Video Ended")


async def audio_process():
    print("Create Audio Started")
    random_execution_time = random.randint(0,8)
    await asyncio.sleep(random_execution_time)
    print("Create Audio Ended")


def mix():
    print("Mix On Video And Audio Started")
    random_execution_time = random.randint(0,8)
    time.sleep(random_execution_time)
    print("Mix On Video And Audio Ended")


async def ai():
    print("AI Process Started")
    await asyncio.gather(video_process(), audio_process())
    mix()
    print("AI Process Ended")


async def printer():
    print("Printer Started")
    random_execution_time = random.randint(0,8)
    await asyncio.sleep(random_execution_time)
    print("Printer Ended")
    

async def main():
    await asyncio.gather(download(), ai(), printer())
    print("All Process Ended Successfully")


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Total Time IS: {total_time}")
