class Job_b:
    def __init__(self, job_id, release, expected,CV,weigth,processing=0):
        # information needed for inizializing a job: id, release, expected processing time, coefficint of variation,  weigths, realization processing time
        self.id = job_id
        self.release = release
        self.processing = processing
        self.expected=expected
        self.CV=CV
        self.we=weigth
        self.alpha_RSOS=None        # Ranomly selected alpha
        self.alpha_DSOS=None        # fixed alpha DSOS
        self.ta_RSOS=None           # alpha-point in RSOS
        self.ta_DSOS=None           # alpha-point in DSOS
        self.done_1=0               # fraction processing time compleated in single machine
        self.MBT=0                  # Mean busy time
        self.comp_RSOS=0            # Complition time job in RSOS algorithm
        self.comp_DSOS=0            # Complition time job in RSOS algorithm


class Job:
    def __init__(self, job_id, release,expected,CV, weigth,processing=0):
        # information needed for inizializing a job: id, release, expected processing time, coefficint of variation,  weigths, realization processing time
        self.id = job_id
        self.release = release
        self.processing = processing
        self.expected=expected
        self.CV=CV
        self.we=weigth
        self.alpha=None           # selcted aloha
        self.ta=None              # alpha point
        self.done_1=0             # fraction processing time compleated in single machine
        self.MBT=0                # Mean busy time
        self.complition=0         # Complition time job
        