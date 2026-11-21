import asyncio

async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f'{name}: {i} sekundi preostalo...')
        await asyncio.sleep(1)
    print(f'{name}: Vrijeme je isteklo!')

async def main():
    timers = [
        asyncio.create_task(timer('Timer 1', 3)),
        asyncio.create_task(timer('Timer 2', 5)),
        asyncio.create_task(timer('Timer 3', 7))
    ]
    await asyncio.gather(*timers)

asyncio.run(main())

# asyncio.run stvara novi event loop
# pokreće se event loop i izvršava proslijeđena korutina (main())
# main() kreira 3 taska (Timer 1-3) - Timer 1 traje 3 sekunde, Timer 2 traje 5 sekundi, Timer 3 traje 7 sekundi
# await asyncio.gather(*timers) omogućava konkurentno izvršavanje (čeka završetak sva tri timera)
# pa tako sva tri timera kreću i ispisuju preostalo vrijeme
# await asyncio.sleep(1) pauzira korutine, a event loop nastavlja izvršavati ostale spremne korutine
# taskovi su u stanju pending cijelo vrijeme (dok čekaju ili se izvršavaju)
# Timer 1 broji 3, 2, 1 i završava se nakon 3 sekunde
# Timer 2 broji 5, 4, 3, 2, 1 i završava se nakon 5 sekundi
# Timer 3 broji 7, 6, 5, 4, 3, 2, 1 i završava se nakon 7 sekundi
# taskovi nakon završetka prelaze u stanje done
# u slučaju da postoji još raspoređenih korutina, event loop će ih izvršavati dokle god ima zadataka za obaviti
# kada se korutine dovrše, event loop se zatvara i svi resursi se oslobađaju
# ukupno izvođenje traje oko 7 sekundi (a ne 15 - zbog konkurentnog izvršavanja)
