def seed_add(seed, value):
    #if the seed is None, normally that uses system time, but I can't add values to a None val
    #So here, grab a system-time-seeded random val instead, and use it for the base seed
    if not seed:
        random.seed(None)
        seed = random.randint(-1000000,1000000)

    return seed + value