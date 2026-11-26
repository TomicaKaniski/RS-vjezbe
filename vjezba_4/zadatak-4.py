import asyncio
import time

aktivni = 0
najvise = 0

async def obradi_zahtjev(broj_zahtjeva, semafor):
    global aktivni, najvise
    
    async with semafor:
        print(f"Zahtjev {broj_zahtjeva} započinje obradu...")
        aktivni += 1
        najvise = max(najvise, aktivni)
        await asyncio.sleep(1)
        print(f"Zahtjev {broj_zahtjeva} je završio obradu.")
        aktivni -= 1
        return broj_zahtjeva

async def main():
    global najvise
    
    for sem in [3, 4]:
        najvise = 0
        
        start = time.perf_counter()
        
        print(f"SEMAFOR = {sem}")
        semafor = asyncio.Semaphore(sem)
        zadaci = [obradi_zahtjev(broj, semafor) for broj in range(1, 9)]
        rezultati = await asyncio.gather(*zadaci)
        
        vrijeme = time.perf_counter() - start
        
        print(f"\nNajveći broj aktivnih zahtjeva: {najvise}\nUkupno vrijeme: {vrijeme:.2f} s\n")

asyncio.run(main())

# Zahtjevi se obrađuju u "valovima" veličine ograničenja.
# Kada imamo ograničenje 3 - imamo tri "vala" (3 + 3 + 2) zahtjeva. Svaki traje 1 s pa je ukupno oko 3 s.
# Kada imamo ograničenje 4 - imamo dva "vala" (4 + 4) zahtjeva. Svaki traje oko 1 s pa je ukupno oko 2 s.
# Općenito:
#   broj "valova" = broj zahtjeva / ograničenje (zaokruženo na više)
#   ukupno vrijeme = broj "valova" * trajanje pojedine obrade

### OUTPUT:
# SEMAFOR = 3
# Zahtjev 1 započinje obradu...
# Zahtjev 2 započinje obradu...
# Zahtjev 3 započinje obradu...
# Zahtjev 1 je završio obradu.
# Zahtjev 2 je završio obradu.
# Zahtjev 3 je završio obradu.
# Zahtjev 4 započinje obradu...
# Zahtjev 5 započinje obradu...
# Zahtjev 6 započinje obradu...
# Zahtjev 4 je završio obradu.
# Zahtjev 5 je završio obradu.
# Zahtjev 6 je završio obradu.
# Zahtjev 7 započinje obradu...
# Zahtjev 8 započinje obradu...
# Zahtjev 7 je završio obradu.
# Zahtjev 8 je završio obradu.

# Najveći broj aktivnih zahtjeva: 3
# Ukupno vrijeme: 3.03 s

# SEMAFOR = 4
# Zahtjev 1 započinje obradu...
# Zahtjev 2 započinje obradu...
# Zahtjev 3 započinje obradu...
# Zahtjev 4 započinje obradu...
# Zahtjev 1 je završio obradu.
# Zahtjev 2 je završio obradu.
# Zahtjev 3 je završio obradu.
# Zahtjev 4 je završio obradu.
# Zahtjev 5 započinje obradu...
# Zahtjev 6 započinje obradu...
# Zahtjev 7 započinje obradu...
# Zahtjev 8 započinje obradu...
# Zahtjev 5 je završio obradu.
# Zahtjev 6 je završio obradu.
# Zahtjev 7 je završio obradu.
# Zahtjev 8 je završio obradu.

# Najveći broj aktivnih zahtjeva: 4
# Ukupno vrijeme: 2.02 s