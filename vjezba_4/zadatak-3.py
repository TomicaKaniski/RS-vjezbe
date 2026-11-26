import asyncio

async def dohvati_brzinu(kamera_id):
    if kamera_id == 1:
        await asyncio.sleep(0.2)
        return 48
    elif kamera_id == 2:
        await asyncio.sleep(2)
        return 65
    elif kamera_id == 3:
        await asyncio.sleep(0.1)
        raise ConnectionError("Kamera je nedostupna!")
    elif kamera_id == 4:
        await asyncio.sleep(0.4)
        return 52

async def obradi_ocitanje(kamera_id):
    try:
        brzina = await asyncio.wait_for(dohvati_brzinu(kamera_id), timeout=1)
        return kamera_id, brzina, None
    except asyncio.TimeoutError:
        return kamera_id, None, "Isteklo vrijeme!"
    except ConnectionError:
        return kamera_id, None, "Kamera je nedostupna!"

async def main():
    ocitanja = [obradi_ocitanje(i) for i in range(1, 5)]
    cit = await asyncio.gather(*ocitanja)
    
    brzine = []
    
    for kamera_id, brzina, razlog in cit:
        if razlog is None:
            print(f"Kamera {kamera_id}: {brzina} km/h")
            brzine.append(brzina)
        else:
            print(f"Kamera {kamera_id}: {razlog}")
        
    if(brzine == []):
        print(f"\nNijedna kamera nema očitanu brzinu!")
    else:
        print(f"\nProsječna brzina je: {sum(brzine)/len(brzine)} km/h")

asyncio.run(main())

# Ako sve četiri kamere zakasne, program će za svaku ispisati "Kamera x: Isteklo vrijeme!".
# Dodatno, na kraju će ispisati i "Nijedna kamera nema očitanu brzinu!" (da izbjegnemo dijeljenje s 0 kod računanja prosječne brzine).

### OUTPUT:
# Kamera 1: 48 km/h
# Kamera 2: Isteklo vrijeme!
# Kamera 3: Kamera je nedostupna!
# Kamera 4: 52 km/h

# Prosječna brzina je: 50.0 km/h
