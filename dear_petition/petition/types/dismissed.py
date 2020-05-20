from django.db.models import Q

from dear_petition.petition.models import OffenseRecord


DISPOSITION_METHODS = (
    "Dismissal without Leave by DA",
    "Dismissed by Court",
    "Deferred Prosecution Dismissal",
    "Discharge and Dismissal",
    "Conditional Discharge",
    "No Probable Cause",
    "Never To Be Served",
)


def get_offense_records(batch):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    qs = qs.filter(build_query())
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CHARGED")
    methods = Q()
    for method in DISPOSITION_METHODS:
        methods |= Q(offense__disposition_method__iexact=method)
    query = action & methods
    return query
