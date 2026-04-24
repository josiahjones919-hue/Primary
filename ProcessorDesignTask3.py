from collections import deque

#Instruction Representation
class Instruction:
    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def __repr__(self):
        return f"{self.addr}"



#Memory Level
class MemoryLevel:
    def __init__(self, name, size, latency, bandwidth):
        self.name = name
        self.size = size
        self.latency = latency
        self.bandwidth = bandwidth

        self.storage = []              #actual stored instructions
        self.queue = deque()           #pending transfers (instr, remaining_latency)

    def is_full(self):
        return len(self.storage) >= self.size

    def add_request(self, instr):
        self.queue.append((instr, self.latency))


#Memory System Controller
class MemorySystem:
    def __init__(self, levels):
        self.levels = levels  #[SSD, DRAM, L3, L2, L1]
        self.clock = 0
        self.trace = []
        self.hits = {lvl.name: 0 for lvl in levels}
        self.misses = {lvl.name: 0 for lvl in levels}

    #Clock Tick
    def tick(self):
        self.clock += 1
        self.trace.append(f"\n--- Cycle {self.clock} ---")

        #Process transfers bottom-up
        for i in range(len(self.levels) - 1):
            self.process_transfer(self.levels[i], self.levels[i + 1])

    #Transfer Logic
    def process_transfer(self, src, dst):
        new_queue = deque()

        moves = 0
        while src.queue and moves < src.bandwidth:
            instr, remaining = src.queue.popleft()

            if remaining > 1:
                new_queue.append((instr, remaining - 1))
            else:
                #Transfer happens
                if dst.is_full():
                    self.evict(dst)

                dst.storage.append(instr)
                self.trace.append(f"{src.name} → {dst.name}: {instr.addr}")
                moves += 1

        src.queue.extendleft(reversed(new_queue))

    #Fetch (Read)
    def fetch(self, addr):
        self.trace.append(f"\nCPU requests {addr}")

        #Search from L1 down to SSD
        for i in reversed(range(len(self.levels))):
            level = self.levels[i]

            for instr in level.storage:
                if instr.addr == addr:
                    self.trace.append(f"HIT at {level.name}")
                    self.hits[level.name] += 1

                    #Promote step-by-step upward
                    self.promote(i, instr)
                    return instr

            self.misses[level.name] += 1

        self.trace.append("MISS: Not found in any level")
        return None

    #Promotion
    def promote(self, level_index, instr):
        for i in range(level_index):
            self.levels[i].add_request(instr)

    #Write Back
    def write_back(self, instr):
        self.trace.append(f"\nWrite-back {instr.addr}")

        for i in range(len(self.levels) - 1):
            self.levels[i].add_request(instr)

    #Eviction (FIFO)
    def evict(self, level):
        evicted = level.storage.pop(0)
        self.trace.append(f"Evicted from {level.name}: {evicted.addr}")

        idx = self.levels.index(level)
        if idx > 0:
            self.levels[idx - 1].add_request(evicted)

    #Run Simulation
    def run_cycles(self, n):
        for _ in range(n):
            self.tick()

    #Output Results
    def print_results(self):
        print("\n CONFIGURATION ")
        for lvl in self.levels:
            print(f"{lvl.name}: Size={lvl.size}")

        print("\n TRACE ")
        for t in self.trace:
            print(t)

        print("\n HITS / MISSES ")
        for lvl in self.levels:
            print(f"{lvl.name}: Hits={self.hits[lvl.name]}, Misses={self.misses[lvl.name]}")

        print("\n FINAL STATE ")
        for lvl in self.levels:
            print(f"{lvl.name}: {lvl.storage}")


if __name__ == "__main__":
    #Create hierarchy (SSD → DRAM → L3 → L2 → L1)
    ssd  = MemoryLevel("SSD", 100, latency=5, bandwidth=2)
    dram = MemoryLevel("DRAM", 50, latency=4, bandwidth=2)
    l3   = MemoryLevel("L3", 20, latency=3, bandwidth=2)
    l2   = MemoryLevel("L2", 10, latency=2, bandwidth=1)
    l1   = MemoryLevel("L1", 5, latency=1, bandwidth=1)

    system = MemorySystem([ssd, dram, l3, l2, l1])

    #Preload SSD with instructions
    for i in range(10):
        ssd.storage.append(Instruction(addr=i, value=i*10))

    #Simulate accesses
    system.fetch(3)
    system.run_cycles(10)

    system.fetch(7)
    system.run_cycles(10)

    system.write_back(Instruction(99, 999))
    system.run_cycles(10)

    #Print
    system.print_results()