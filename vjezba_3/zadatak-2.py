import asyncio
import time

async def dohvati_korisnike():
    korisnici = [
        {"ime": "Ana",  "prezime": "Anić"},
        {"ime": "Ivan", "prezime": "Ivanić"},
        {"ime": "Marko", "prezime": "Markić"},
        {"ime": "Petar",  "prezime": "Perić"}
    ]
    await asyncio.sleep(3)
    return korisnici

async def dohvati_proizvode():
    proizvodi = [
        {"id": "1",  "naziv": "Brašno"},
        {"id": "2",  "naziv": "Šećer"},
        {"id": "3",  "naziv": "Jaja"}
    ]
    await asyncio.sleep(5)
    return proizvodi

async def main():    
    podaci_1, podaci_2 = await asyncio.gather(dohvati_korisnike(), dohvati_proizvode())
    print(f'Korisnici: {podaci_1}')
    print(f'Proizvodi: {podaci_2}')

t1 = time.perf_counter()
asyncio.run(main())
t2 = time.perf_counter()
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")
