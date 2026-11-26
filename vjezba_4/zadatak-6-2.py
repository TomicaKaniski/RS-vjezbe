import aiohttp
import asyncio

async def dohvati_cinjenicu(klijent, broj_zahtjeva, pokusaj):
    async with klijent.get("https://catfact.ninja/fact") as odgovor:
        if odgovor.status != 200:
            return (odgovor.status, None)
        
        podaci = await odgovor.json()
        return (200, podaci["fact"])
    
async def dohvati_s_ponavljanjem(klijent, broj_zahtjeva, semafor):
    odgoda = 0.5
    
    for pokusaj in range(1, 4):
        async with semafor:
            try:
                status, cinjenica = await asyncio.wait_for(dohvati_cinjenicu(klijent, broj_zahtjeva, pokusaj), timeout = 2)
            except asyncio.TimeoutError:
                status, cinjenica = "timeout", None

        if status == 200:
            return broj_zahtjeva, pokusaj, cinjenica, None
        if status != "timeout" and status != 503:
            return broj_zahtjeva, pokusaj, None, f"status {status}"

        if pokusaj < 3:
            await asyncio.sleep(odgoda)
            odgoda *= 2

    return broj_zahtjeva, 3, None, f"Neuspjeh nakon 3 pokušaja ({status})."

async def main():
    semafor = asyncio.Semaphore(3)
    dohvaceno = 0
    neuspjesno = 0
    ukupno_pokusaja = 0
    
    print("STVARNI API:")
    
    async with aiohttp.ClientSession() as klijent:
        cinjenice = [dohvati_s_ponavljanjem(klijent, broj, semafor) for broj in range(1, 9)]
        rezultati = await asyncio.gather(*cinjenice)
        
    for broj, pokusaji, cinjenica, razlog in rezultati:
        ukupno_pokusaja += pokusaji
        if razlog is None:
            dohvaceno += 1
            print(f"Zahtjev {broj} ({pokusaji} pok.): {cinjenica}")
        else:
            neuspjesno += 1
            print(f"Zahtjev {broj} ({pokusaji} pok.): {razlog}")
    
    print(f"\nDohvaćeno: {dohvaceno}")
    print(f"Neuspješno: {neuspjesno}")
    print(f"Ukupno pokušaja: {ukupno_pokusaja}")

asyncio.run(main())

### OUTPUTS:
# STVARNI API:
# Zahtjev 1 (1 pok.): About 37% of American homes today have at least 1 cat.
# Zahtjev 2 (1 pok.): Normal body temperature for a cat is 102 degrees F.
# Zahtjev 3 (1 pok.): The life expectancy of cats has nearly doubled since 1930 - from 8 to 16 years.
# Zahtjev 4 (1 pok.): Since cats are so good at hiding illness, even a single instance of a symptom should be taken very seriously.
# Zahtjev 5 (1 pok.): Cats often overract to unexpected stimuli because of their extremely sensitive nervous system.
# Zahtjev 6 (1 pok.): Cats have 30 vertebrae (humans have 33 vertebrae during early development; 26 after the sacral and coccygeal regions fuse)
# Zahtjev 7 (1 pok.): Your cat's heart beats at a rate almost double that of yours, from 110-140 beats per minute.
# Zahtjev 8 (1 pok.): The cat's footpads absorb the shocks of the landing when the cat jumps.

# Dohvaćeno: 8
# Neuspješno: 0
# Ukupno pokušaja: 8
