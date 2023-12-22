class Job_b:
    def __init__(self, job_id, release, expected,CV,weigth,processing=0,alpha=None,MBT=0):
        # information needed for single machine: id, release, expected processing time, weigths
        self.id = job_id
        self.release = release
        self.processing = processing
        self.expected=expected
        self.CV=CV
        self.we=weigth
        self.alpha_RSOS=None
        self.alpha_DSOS=None
        self.ta_RSOS=None
        self.ta_DSOS=None
        self.done_1=0
        self.MBT=0
        self.comp_RSOS=0
        self.comp_DSOS=0


class Job:
    def __init__(self, job_id, release,expected,CV, weigth,processing=0,alpha=None,MBT=0):
        # information needed for single machine: id, release, expected processing time, weigths
        self.id = job_id
        self.release = release
        self.processing = processing
        self.expected=expected
        self.CV=CV
        self.we=weigth
        self.alpha=None
        self.ta=None
        self.done_1=0
        self.MBT=0
        self.complition=0
        