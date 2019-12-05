import json

class SettingParser:

    def __init__(self, filename, worker_manager, task_manager, data):

        with open(filename) as json_file:
            settings = json.load(json_file)
            self.original = settings
            if "pid" in settings.keys():
                self.pid = settings["pid"]

            if "file" in settings.keys():
                "TODO"
                # read_data(args[1])
            if "price" in settings.keys():
                data.price = float(settings["price"])
            if "n_judgements" in settings.keys():
                data.n_judgements = int(settings["n_judgements"])

            if "worker_arrival_interval" in settings.keys():
                worker_manager.worker_arrival_interval = int(settings["worker_arrival_interval"])
            if "worker_classification" in settings.keys():
                worker_manager.worker_classification = int(settings["worker_classification"])
            if "worker_property_names" in settings.keys():
                worker_manager.worker_property_names = settings["worker_property_names"]
                if "worker_properties" in settings.keys():
                    worker_manager.worker_properties = settings["worker_properties"]
                    for i in range(len(worker_manager.worker_properties)):
                        p = worker_manager.worker_properties[i]
                        for j in range(len(p)):
                            try:
                                worker_manager.worker_properties[i][j] = float(p[j])
                                if float(p[j]).is_integer():
                                    worker_manager.worker_properties[i][j] = int(p[j])
                            except ValueError:
                                worker_manager.worker_properties[i][j] = p[j]
                    worker_manager.worker_classification_name = settings["worker_properties"][settings["worker_property_names"].index("class_name")]
                    worker_manager.worker_distribution = worker_manager.worker_properties[settings["worker_property_names"].index("distribution")]

            if "worker_manager.dropout_time" in settings.keys():
                worker_manager.dropout_time = int(settings["dropout_time"])

            if "runtime" in settings.keys():
                self.runtime = int(settings["runtime"])
            if "time_stamp" in settings.keys():
                self.time_stamp = int(settings["time_stamp"])
            if "repeat_times" in settings.keys():
                self.repeat_times = int(settings["repeat_times"])

            if "n_data_rows" in settings.keys():
                task_manager.n_data_rows = int(settings["n_data_rows"])
            if "data_selection" in settings.keys():
                task_manager.data_selection = settings["data_selection"]
            if "task_assignment" in settings.keys():
                task_manager.assign = settings["task_assignment"]
            # if "worker_selection" in settings.keys():
            #     something = settings["worker_selection"]
