import asyncio

async def dohvati_podatke():
    brojevi = [i for i in range(1, 11)]
    await asyncio.sleep(3)
    print(f"Podaci dohvaćeni")
    return brojevi

async def main():
    podaci = await dohvati_podatke()
    print(podaci)

asyncio.run(main())
