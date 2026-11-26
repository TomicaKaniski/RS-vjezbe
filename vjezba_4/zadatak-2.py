import aiohttp
import asyncio

async def dohvati_cinjenicu(klijent, broj_zahtjeva):
    async with klijent.get("https://catfact.ninja/fact") as odgovor:
        odgovor.raise_for_status()
        podaci = await odgovor.json()
    print(f"Primljen odgovor na zahtjev {broj_zahtjeva}.")
    return broj_zahtjeva, podaci["fact"], podaci["length"]

async def main():
    async with aiohttp.ClientSession() as session:
        cinjenice = [dohvati_cinjenicu(session, broj) for broj in range(1, 6)]
        facts = await asyncio.gather(*cinjenice)

        najdulja = facts[0]
        for f in facts:
            if f[2] > najdulja[2]:
                najdulja = f

        print(f"\nNajdulja činjenica (zahtjev {najdulja[0]}, duljina {najdulja[2]}):\n{najdulja[1]}")

asyncio.run(main())

### OUTPUTS:
# Primljen odgovor na zahtjev 3.
# Primljen odgovor na zahtjev 1.
# Primljen odgovor na zahtjev 4.
# Primljen odgovor na zahtjev 2.
# Primljen odgovor na zahtjev 5.

# Najdulja činjenica (zahtjev 2, duljina 217):
# The most traveled cat is Hamlet, who escaped from his carrier while on a flight. He hid for seven weeks behind a panel on the airplane. By the time he was discovered, he had traveled nearly 373,000 miles (600,000 km).
