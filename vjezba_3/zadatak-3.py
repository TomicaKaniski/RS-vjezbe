import asyncio

baza_korisnika = [
    {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
    {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
    {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
    {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]

baza_lozinka = [
    {'korisnicko_ime': 'mirko123', 'lozinka': 'lozinka123'},
    {'korisnicko_ime': 'ana_anic', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'maja_0x', 'lozinka': 's324SDFfdsj234'},
    {'korisnicko_ime': 'zdeslav032', 'lozinka': 'deso123'}
]

async def autentifikacija(korisnik: dict):
    korisnicko_ime = korisnik.get("korisnicko_ime")
    email = korisnik.get("email")
    lozinka = korisnik.get("lozinka")

    await asyncio.sleep(3)
    
    for zapis in baza_korisnika:
        if zapis["korisnicko_ime"] == korisnicko_ime and zapis["email"] == email:
            return await autorizacija(zapis, lozinka)

    return f"Korisnik {korisnik} nije pronađen."

async def autorizacija(korisnik: dict, lozinka):
    korisnicko_ime = korisnik.get("korisnicko_ime")

    await asyncio.sleep(2)
    
    for zapis in baza_lozinka:
        if zapis["korisnicko_ime"] == korisnicko_ime and zapis["lozinka"] == lozinka:
            return f"Korisnik {korisnik}: Autorizacija uspješna."

    return f"Korisnik {korisnik}: Autorizacija neuspješna."

async def main():
    auth = await autentifikacija({"korisnicko_ime": "ana_anic", "email": "aanic@gmail.com", "lozinka": "super_teska_lozinka"})
    return auth

print(asyncio.run(main()))
