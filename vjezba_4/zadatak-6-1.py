import aiohttp
import asyncio

async def dohvati_cinjenicu(klijent, broj_zahtjeva, pokusaj):
    if broj_zahtjeva == 2 and pokusaj == 1:
        await asyncio.sleep(5)

    if broj_zahtjeva == 5:
        return (503, None)
    
    await asyncio.sleep(0.1)
    
    return (200, f"Činjenica {broj_zahtjeva}")

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
    
    print("SIMULACIJA:")
    
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
# SIMULACIJA:
# Zahtjev 1 (1 pok.): Činjenica 1
# Zahtjev 2 (2 pok.): Činjenica 2
# Zahtjev 3 (1 pok.): Činjenica 3
# Zahtjev 4 (1 pok.): Činjenica 4
# Zahtjev 5 (3 pok.): Neuspjeh nakon 3 pokušaja (503).
# Zahtjev 6 (1 pok.): Činjenica 6
# Zahtjev 7 (1 pok.): Činjenica 7
# Zahtjev 8 (1 pok.): Činjenica 8

# Dohvaćeno: 7
# Neuspješno: 1
# Ukupno pokušaja: 11
