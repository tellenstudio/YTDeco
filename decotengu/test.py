import decotengu

def test_1():
    engine = decotengu.create()
    engine.add_gas(0, 21)

    profile = engine.calculate(35, 40)

    for step in profile:
        print(step)

    for stop in engine.deco_table:
        print(stop)

    print(engine.deco_table.total)

def test_2():
    engine = decotengu.create()
    engine.add_gas(0, 21)
    engine.model = decotengu.ZH_L16C_GF()
    engine.model.gf_low = 0.2    # vs. 0.30 - first stop deeper
    engine.model.gf_high = 0.90  # vs. 0.85 - last stop shorter

    profile = engine.calculate(35, 40)
    # list(profile)
    for step in profile:
        print(step)

    print(engine.deco_table.total)
    print(engine.deco_table[0])
    print(engine.deco_table[-1])

if __name__ == '__main__':
    # test_1()
    test_2()
