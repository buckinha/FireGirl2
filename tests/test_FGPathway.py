#test scripts for FGPathway

from firegirl2 import FGPathway
import math, random

def test_initialization():
    #possible input args are: landscape_size=(129,129), random_seed=None
    pw1 = FGPathway.FGPathway()

    #testing that random_seed=None produces different landscapes each time
    for i in range(20):
        pw_a = FGPathway.FGPathway(random_seed=None)
        pw_b = FGPathway.FGPathway(random_seed=None)

        #test the grids to make sure they are different
        assert (pw_a.site_index != pw_b.site_index).any()
        assert (pw_a.stand_init_yr != pw_b.stand_init_yr).any()
        assert (pw_a.stand_rplc_fire_yr != pw_b.stand_rplc_fire_yr).any()
        assert (pw_a.surf_fire_yr != pw_b.surf_fire_yr).any()

    #testing that random_seed is used as intended
    for i in range(20):
        val1 = random.random()
        val2 = random.random()
        pw_a = FGPathway.FGPathway(random_seed=val1)
        pw_b = FGPathway.FGPathway(random_seed=val2)
        pw_c = FGPathway.FGPathway(random_seed=val2)

        #for a and b, test the grids to make sure they are different
        assert (pw_a.site_index != pw_b.site_index).any()
        assert (pw_a.stand_init_yr != pw_b.stand_init_yr).any()
        assert (pw_a.stand_rplc_fire_yr != pw_b.stand_rplc_fire_yr).any()
        assert (pw_a.surf_fire_yr != pw_b.surf_fire_yr).any()

        #for b and c, test the grids to make sure they are the same
        assert (pw_c.site_index == pw_b.site_index).all()
        assert (pw_c.stand_init_yr == pw_b.stand_init_yr).all()
        assert (pw_c.stand_rplc_fire_yr == pw_b.stand_rplc_fire_yr).all()
        assert (pw_c.surf_fire_yr == pw_b.surf_fire_yr).all()

    #testing landscape sizing
    for i in range(20):
        #square sizes
        s = random.randint(1,500)
        pw = FGPathway.FGPathway(landscape_size=s)
        assert pw.size == (s,s)
        assert len(pw.site_index) == s
        assert len(pw.site_index[0]) == s
        assert len(pw.stand_init_yr) == s
        assert len(pw.stand_init_yr[0]) == s
        assert len(pw.stand_rplc_fire_yr) == s
        assert len(pw.stand_rplc_fire_yr[0]) == s
        assert len(pw.surf_fire_yr) == s
        assert len(pw.surf_fire_yr[0]) == s

    #random sizes
    for i in range(20):
        s1 = random.randint(1,500)
        s2 = random.randint(1,500)
        pw = FGPathway.FGPathway(landscape_size=[s1,s2])
        assert pw.size == (s1,s2)
        assert len(pw.site_index) == s1
        assert len(pw.site_index[0]) == s2
        assert len(pw.stand_init_yr) == s1
        assert len(pw.stand_init_yr[0]) == s2
        assert len(pw.stand_rplc_fire_yr) == s1
        assert len(pw.stand_rplc_fire_yr[0]) == s2
        assert len(pw.surf_fire_yr) == s1
        assert len(pw.surf_fire_yr[0]) == s2


def test_get_surface_fuel():
    for i in range(20):
        pw = FGPathway.FGPathway()
        for i in range(pw.size[0]):
            for j in range(pw.size[1]):
                fuel = pw.get_surface_fuel([i,j])
                assert fuel >= 0.0
                assert fuel < 5.0 #out of curiousity

def test_get_ladder_fuel():
    for i in range(20):
        pw = FGPathway.FGPathway()
        for i in range(pw.size[0]):
            for j in range(pw.size[1]):
                fuel = pw.get_surface_fuel([i,j])
                assert fuel >= 0.0
                assert fuel < 5.0 #out of curiousity

def test_age_functions():
    for i in range(20):
        pw = FGPathway.FGPathway()
        for i in range(pw.size[0]):
            for j in range(pw.size[1]):
                stand_age = pw.get_age([i,j])
                yrs_since_fire = pw.get_years_since_fire([i,j])

                assert stand_age >= 0
                assert yrs_since_fire >= 0


def test_simulate():
    for i in range(20):
        pw = FGPathway.FGPathway()
        years1 = random.randint(0,150)
        years2 = random.randint(0,150)
        pw.simulate(years=years1)
        pw.simulate(years=years2)

        assert pw.current_year == years1 + years2
        assert len(pw.year_history) == years1 + years2


def all_tests():
    test_initialization()
    test_get_surface_fuel()
    test_get_ladder_fuel()
    test_age_functions()
    test_simulate()


if __name__ == "__main__":
    all_tests()