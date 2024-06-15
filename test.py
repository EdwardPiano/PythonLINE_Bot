import asyncio
import time


async def get_data():
    await asyncio.sleep(2)  # 模拟耗时操作
    return "data"


async def main():
    start_time = time.time()
    print(start_time)
    task1 = asyncio.create_task(get_data())
    task2 = asyncio.create_task(get_data())
    await task1
    await task2
    print(f"Total time: {time.time() - start_time}")


if __name__ == "__main__":
    asyncio.run(main())


# import time


# def get_data():
#     time.sleep(2)  # 模拟耗时操作
#     return "data"


# def main():
#     start_time = time.time()
#     data1 = get_data()
#     data2 = get_data()
#     print(f"Total time: {time.time() - start_time}")


# if __name__ == "__main__":
#     main()
