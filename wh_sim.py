# Steps to get from warehouse
# 1. WH to robotrain
# 2. robotrain to each station
#
# Assumptions
# ===========
# 1. Equal probability distribution for location within WH
# 2. Likelihood of waiting for robotrain is function of current pallets/hour
# 3. No queueing of pallets between station and robotrain
#
# Montecarlo simulation counting the max number of pallets "on the floor"
# during a one day production period
#
# Output: Number of stations that would cover 95% of production
#
# Sim1: IO01 used for Prod 1 in
# Sim2: All Prod1 pallets through IO03


# Constants
ADSM_THROUGHPUT = 6  # pallets per hour
PALLET_PER_LOT = 50  # pallets in a lot
DRYING_TIME = 15     # time needed to clear condensation

# Global variables
using_IO01 = True

# sim constants: [simulated_runs, use_IO01]
sims = [
    [100, True, 7, 2],
    [100, False, 7, 2],
    [100, False, 8, 2]
]


class ADSM:
    # machine states
    PREP = 0
    RUNNING = 1
    REQUESTING = 2
    STARVED = 3
    COMPLETE = 4  # status when processed pallet count reaches target value

    status: int  # current machine state
    processed_pallets: int  # count of insepected pallets
    pallets_in_lot: int
    last_status: int

    time_left_on_pallet: int

    def __init__(self, lot_size = 50):
        self.status = self.PREP
        self.last_status = self.status
        self.processed_pallets = 0
        self.pallets_in_lot = lot_size
    
    # this update should be called every time increment
    def update(self):
        if self.processed_pallets >= self.pallets_in_lot:
            self.status = self.COMPLETE
        elif self.status == self.PREP:
            # nothing to do
            pass
        elif self.status == self.RUNNING:
            # decrement time left on pallet
            # if pallet completes change status to requesting
            pass
        elif self.status == self.REQUESTING:
            # if requesting for 2 or more iterations change status to starved
            pass
        elif self.status == self.STARVED:
            # increment starved timer TODO: add starved timer
            # increase starved count  -->  this will identify required buffer
            pass

    def feed_pallet(self):
        pass

    def set_status(self, s):
        self.status = s
    
    def get_status(self):
        return self.status
    
    def increment_pallet_count(self):
        self.processed_pallets += 1
        if self.processed_pallets >= self.pallets_in_lot:
            self.set_status(self.COMPLETE)


class DryingStation:

    dry_time: int  # how long a pallet must be in the drying station before use
    num_drying_stations: int  # number of spots for drying pallets
    drying_times_per_pallet = []

    can_supply: bool  # at least one pallet in station longer than drying time
    pallet_count: int  # number of pallets in drying station
    dried_count: int  # number of pallets that have been dried

    def __init__(self, drying_time = 15, num_drying_stations = 1):
        self.can_supply = False
        self.pallet_count = 0
        self.dry_time = drying_time
        self.num_drying_stations = num_drying_stations
    
    # this update should be called every time increment 
    def update(self):
        for t in self.drying_times_per_pallet:
            t -= 1
        if self.drying_times_per_pallet and min(self.drying_times_per_pallet) <= 0:
            self.can_supply = True

    def add_pallet(self):
        self.pallet_count += 1
        self.drying_times_per_pallet.append(self.dry_time)

    def supply_pallet(self):
        if self.can_supply:
            self.pallet_count -= 1
            self.drying_times_per_pallet.pop()
    
    def is_drying(self):
        if self.drying_times_per_pallet:
            return True
        else:
            return False

    def is_full(self):
        if self.pallet_count >= self.num_drying_stations:
            return True
        else:
            return False

class Callback():

    timeout: int
    callback: callable

    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback

    def update(self):
        if timeout > 0:
            timeout -= 1
        else:
            self.callback()


def get_time_from_wh_to_robotrain():
    pass

def get_time_waiting_for_robotrain(time):
    pass

def run_simulation(sim_parameters):
    simulated_runs = sim_parameters[0]
    using_IO01 = sim_parameters[1]
    start_time = sim_parameters[2]
    num_drying_stations = sim_parameters[3]

    adsm: ADSM
    drying_station: DryingStation

    for r in range(simulated_runs):
        
        callbacks = []
        adsm = ADSM(PALLET_PER_LOT)
        drying_station = DryingStation(DRYING_TIME, num_drying_stations)
        
        max_num_pallets_on_floor = 0
        current_pallets_on_floor = 0
        time_elapsed = 0

        while adsm.get_status() != ADSM.COMPLETE and current_pallets_on_floor != 0:
            
            adsm.update()
            drying_station.update()
            for call in callbacks:
                call.update()

            requested_pallets = 0

            def decrement_requested_pallets():
                requested_pallets -= 1

            # get pallet from WH if space in drying station
            if not drying_station.is_full and (drying_station.pallet_count + requested_pallets) <= drying_station.num_drying_stations:
                requested_pallets += 1
                callbacks.append(get_time_to_IO02()
            # start processing a pallet
            if drying_station.can_supply:
                if adsm.get_status != ADSM.RUNNING:
                    drying_station.supply_pallet()
                    adsm.feed_pallet()
            
            # check if any pallets ready for processing
            # if not get time to receive pallet
                # wait time and update drying station
            # if available
                # if 
            time_elapsed += 1

for sim in sims:
    run_simulation(sim)
