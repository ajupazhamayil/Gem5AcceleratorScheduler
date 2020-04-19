#include "debug/FPGAScheduler.hh"
#include "fpga-scheduler/fpgascheduler.hh"

FPGAScheduler::FPGAScheduler(FPGASchedulerParams *params) :
    SimObject(params), policy_num(params->policy)//latency(params->time_to_process)
{
    DPRINTF(FPGAScheduler, "Created the FPGAScheduler object\n");
}

void
FPGAScheduler::startup()
{
    DPRINTF(FPGAScheduler, "Starting up the FPGAScheduler object");
}

void
FPGAScheduler::setCPU(FpgaCPU *_cpu){
  this->cpu = _cpu;
}

void
FPGAScheduler::shortestJobFirst()
{ 

  TaskHashes.sort([](pair<uint64_t,uint64_t> const& a, pair<uint64_t,uint64_t> const& b) {
      return a.second < b.second;
  });

}

void
FPGAScheduler::longestJobFirst()
{ 

  TaskHashes.sort([](pair<uint64_t,uint64_t> const& a, pair<uint64_t,uint64_t> const& b) {
      return a.second > b.second;
  });

}

void
FPGAScheduler::insertProcess(uint64_t val, uint64_t size)
{
    TaskHashes.push_back(make_pair(val, size));
    for (auto it:TaskHashes){
        DPRINTF(FPGAScheduler, "\n InsertedHash=%lu    InsertedSize=%lu \n",
        it.first, it.second);
    }
}

uint64_t FPGAScheduler::popProcess()
{
    switch(policy_num){
        case 1: this->shortestJobFirst(); DPRINTF(FPGAScheduler, "shortestJobFirst"); break;
        case 2: this->longestJobFirst(); DPRINTF(FPGAScheduler, "longestJobFirst"); break;
        default: DPRINTF(FPGAScheduler, "shortestJobFirst"); break;
    }
    
    DPRINTF(FPGAScheduler, "\n isTaskHashesEmpty=%d    currentFront=%lu \n", 
    TaskHashes.empty(), TaskHashes.front().first);
    uint64_t hash = TaskHashes.front().first;
    return hash;
}

void
FPGAScheduler::deleteProcess()
{
    TaskHashes.pop_front();
    DPRINTF(FPGAScheduler, "Scheduling the FPGAScheduler event\n");
}

bool
FPGAScheduler::is_TaskHashesEmpty()
{
    return TaskHashes.empty();
}

Tick 
FPGAScheduler::getLatency()
{
    uint64_t size = this->TaskHashes.size();
    this->latency = size*size;
    DPRINTF(FPGAScheduler, "Scheduling latency is %lu ticks (ps)\n", this->latency);
    return this->latency;
}

FPGAScheduler*
FPGASchedulerParams::create()
{
    return new FPGAScheduler(this);
}
