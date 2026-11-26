import asyncio

cekaj = 0.8 # mijenjam kod pokušaja

async def dohvati_brzinu(pokusaj):
    if pokusaj == 1:
        await asyncio.sleep(0.8)
    elif pokusaj == 2:
        await asyncio.sleep(0.6)
    elif pokusaj == 3:
        await asyncio.sleep(cekaj)
    return 54

async def dohvati_s_ponavljanjem():
    odgoda = 0.5
    
    print(f"Pokušaj 3 čeka {cekaj}:")
    
    for pokusaj in range(1, 4):
        try:
            brzina = await asyncio.wait_for(dohvati_brzinu(pokusaj), timeout=0.3)
            print(f"Pokušaj {pokusaj} je uspio.")
            return brzina
        except asyncio.TimeoutError:
            print(f"Pokušaj {pokusaj} je istekao!")
            
            if (pokusaj < 3):
                await asyncio.sleep(odgoda)
                odgoda *= 2
    print("Svi pokušaji su neuspješni!")
    return None

async def main():
    brzina = await dohvati_s_ponavljanjem()
    if (brzina is not None):
        print(f"Brzina je {brzina} km/h.")

asyncio.run(main())

# 2. slučaj (pokušaj 3 čeka 0.8 s):
# Klijent je poslao 3 zahtjeva, a između pokušaja je čekao 2 puta (0.5 s i 1 s).
# Nakon trećeg isteka odmah javlja neuspjeh.

### OUTPUT:
# Pokušaj 3 čeka 0.1:
# Pokušaj 1 je istekao!
# Pokušaj 2 je istekao!
# Pokušaj 3 je uspio.
# Brzina je 54 km/h.

# Pokušaj 3 čeka 0.8:
# Pokušaj 1 je istekao!
# Pokušaj 2 je istekao!
# Pokušaj 3 je istekao!
# Svi pokušaji su neuspješni!
