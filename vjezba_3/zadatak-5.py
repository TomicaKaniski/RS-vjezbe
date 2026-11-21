import asyncio

osjetljivi_podaci = [
    {"prezime": "Anić", "broj_kartice": 1234567890, "CVV": 123},
    {"prezime": "Perić", "broj_kartice": 2345678901, "CVV": 456},
    {"prezime": "Vidrić", "broj_kartice": 3456789012, "CVV": 789}
]

async def secure_data(podaci: dict):
    prezime = podaci.get("prezime")
    broj_kartice = podaci.get("broj_kartice")
    broj_kartice_enc = hash(str(broj_kartice))
    CVV = podaci.get("CVV")
    CVV_enc = hash(str(CVV))

    await asyncio.sleep(3)
    
    return {"prezime": prezime, "broj_kartice": broj_kartice_enc, "CVV": CVV_enc}

async def main():
    zadaci = [asyncio.create_task(secure_data(podatak)) for podatak in osjetljivi_podaci]
    
    rezultati = await asyncio.gather(*zadaci)
    for rezultat in rezultati:
        print(rezultat)

asyncio.run(main())
