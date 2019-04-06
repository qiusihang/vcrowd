def data_selection(data):
####################

    "Do nothing"

####################


def execute(worker, task):
####################

    return 300

####################


def assign(worker_manager, task_manager, data):
####################

    worker = wm.return_upcoming_worker()
    task = tm.return_upcoming_task()
    return (worker, task)

####################
