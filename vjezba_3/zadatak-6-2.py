# import asyncio, time

# async def fetch_data(param):
#     print(f"Nešto radim s {param}...")
#     await asyncio.sleep(param)
#     print(f'Dovršio sam s {param}.')
#     return f"Rezultat za {param}"

# async def main():
#     task1 = asyncio.create_task(fetch_data(1)) # schedule
#     task2 = asyncio.create_task(fetch_data(2)) #schedule
#     result1 = await task1
#     print("Fetch 1 uspješno završen.")
#     return [result1]

# t1 = time.perf_counter()
# results = asyncio.run(main()) # pokretanje event loop-a
# t2 = time.perf_counter()
# print(results)
# print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")


# način 2 - držati event loop busy (sleep >= 1)
import asyncio, time

async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(param)
    print(f'Dovršio sam s {param}.')
    return f"Rezultat za {param}"

async def main():
    task1 = asyncio.create_task(fetch_data(1)) # schedule
    task2 = asyncio.create_task(fetch_data(2)) #schedule
    result1 = await task1
    print("Fetch 1 uspješno završen.")
    
    await asyncio.sleep(2)

    return [result1]

t1 = time.perf_counter()
results = asyncio.run(main()) # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")
