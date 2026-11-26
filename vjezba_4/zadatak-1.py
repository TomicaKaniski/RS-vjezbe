import asyncio
import time

async def posalji_zahtjev(kamera_id, trajanje):
    print(f"Prikupljam podatke sa kamere {kamera_id}...")
    await asyncio.sleep(trajanje)
    print(f"Podaci sa kamere {kamera_id} prikupljeni.")
    return f"Podaci sa kamere {kamera_id}"

async def main():
    kamera_ids = [1, 2, 3]
    trajanja = [3, 1, 2]

    start = time.perf_counter()
    print("SEKVENCIJALNO:") 
    for i in range(len(kamera_ids)):
        await posalji_zahtjev(kamera_ids[i], trajanja[i])
    end = time.perf_counter()
    print(f"SEKVENCIJALNO izvršavanje traje {end - start:.2f} s.\n")

    start = time.perf_counter()
    print("KONKURENTNO:") 
    zahtjevi = [posalji_zahtjev(kamera_ids[i], trajanja[i]) for i in range(len(kamera_ids))]
    rezultati = await asyncio.gather(*zahtjevi)
    end = time.perf_counter()
    
    print(rezultati)
    print(f"KONKURENTNO izvršavanje traje {end - start:.2f} s.\n")

asyncio.run(main())

# Predviđanje:
# - sekvencijalno oko 6s (vremena se zbrajaju)
# - konkurentno oko 3s (najsporiji zahtjev)

# Odgovori stižu redom 2, 3, 1 (kako završavaju).
# gather() vraća rezultate redom kojim su korutine predane (1, 2, 3) (neovisno koja je prva završila)

### OUTPUTS:
# SEKVENCIJALNO:
# Prikupljam podatke sa kamere 1...
# Podaci sa kamere 1 prikupljeni.
# Prikupljam podatke sa kamere 2...
# Podaci sa kamere 2 prikupljeni.
# Prikupljam podatke sa kamere 3...
# Podaci sa kamere 3 prikupljeni.
# SEKVENCIJALNO izvršavanje traje 6.03 s.

# KONKURENTNO:
# Prikupljam podatke sa kamere 1...
# Prikupljam podatke sa kamere 2...
# Prikupljam podatke sa kamere 3...
# Podaci sa kamere 2 prikupljeni.
# Podaci sa kamere 3 prikupljeni.
# Podaci sa kamere 1 prikupljeni.
# ['Podaci sa kamere 1', 'Podaci sa kamere 2', 'Podaci sa kamere 3']
# KONKURENTNO izvršavanje traje 3.01 s.
