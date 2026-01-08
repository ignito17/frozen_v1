from time import perf_counter
import resource

# An importable class to measure runtime and resource usages of python process
class JobMetrics:
    def __enter__(self):
        self.start=perf_counter()
        self.start_rusage=resource.getrusage(resource.RUSAGE_SELF)
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.end=perf_counter()
        self.end_rusage=resource.getrusage(resource.RUSAGE_SELF)

    def report(self):
        return{
            # Time in Seconds
            # Wall clock
            "runtime_secs": self.end - self.start,
            # CPU --- Total Process
            "cpu_user_total_secs": self.end_rusage.ru_utime,
            "cpu_sys_total_secs": self.end_rusage.ru_stime,
            # CPU --- This job only, i.e. after __enter__ was called
            "cpu_user_job_secs": self.end_rusage.ru_utime - self.start_rusage.ru_utime,
            "cpu_sys_job_secs": self.end_rusage.ru_stime - self.start_rusage.ru_stime,
            # Memory
            # Whole Process Maximum Resident Set Size in KB
            "max_rss_total_kb": self.end_rusage.ru_maxrss,
            # After the __enter__ was called
            "max_rss_job_kb": max(0, self.end_rusage.ru_maxrss - self.start_rusage.ru_maxrss),
            }