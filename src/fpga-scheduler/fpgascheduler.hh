#ifndef __SCHEDULER_FPGA_SCHEDULER_OBJECT_HH__
#define __SCHEDULER_FPGA_SCHEDULER_OBJECT_HH__

#include "params/FPGAScheduler.hh"
#include "sim/sim_object.hh"
#include "cpu/fpgacpu/fpgacpu.hh"

class FPGAScheduler : public SimObject
{
  private:
    FpgaCPU *cpu;
    // Array to queue the TaskHashes which requests the FPGA
    std::list< std::pair<uint64_t, uint64_t> > TaskHashes;
  public:
    void deleteProcess();
    uint64_t popProcess();
    Tick getLatency();
    void insertProcess(uint64_t, uint64_t);
    // TODO More scheduling algorithms
    void shortestJobFirst();
    void longestJobFirst();
    void setCPU(FpgaCPU *_cpu);
    bool is_TaskHashesEmpty();
    // inProcTime+sorting+outProcTime
    Tick latency;
    uint64_t policy_num;
    FPGAScheduler(FPGASchedulerParams *p);
    void startup();
};

#endif // __SCHEDULER_FPGA_SCHEDULER_OBJECT_HH__
