import asyncio
async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return "hello"

async def main():
    print("main开始")
    # task_list = [
    #     asyncio.create_task(func(),name="n1"),
    #     asyncio.create_task(func(),name="n2")
    # ]
    task_list = [
       func(),
       func()
    ]
    print("main结束")
    done,pending = await asyncio.wait(task_list,timeout=None)
    print(done,pending)
    
asyncio.run(main())
    