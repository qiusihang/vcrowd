
class SettingParser:

    def __init__(self, filename, worker_manager, task_manager, data):

        for line in open(filename):
            line = line.replace(' ','')
            line = line.replace('\n','')
            line = line.replace('\r','')
            if len(line) < 1:
                continue
            if line[0] != '#':
                args = line.split('=')

                if args[0] == "data.file":
                    "TODO"
                    # read_data(args[1])
                elif args[0] == "data.n_judgements":
                    data.n_judgements = int(args[1])

                elif args[0] == "task_manager.n_data_rows":
                    task_manager.n_data_rows = int(args[1])
                elif args[0] == "task_manager.data_selection":
                    task_manager.data_selection = args[1]
                elif args[0] == "task_assignment.assign":
                    task_manager.assign = args[1]

                elif args[0] == "worker_manager.execute":
                    worker_manager.execute = args[1]
                elif args[0] == "worker_manager.worker_arrival_interval":
                    worker_manager.worker_arrival_interval = int(args[1])
                elif args[0] == "worker_manager.worker_classification":
                    worker_manager.dropout_time = int(args[1])
                elif args[0] == "worker_manager.worker_classification_name":
                    worker_manager.worker_classification_name = args[1].split(',')
                elif args[0] == "worker_manager.worker_distribution":
                    params = args[1].split(',')
                    worker_manager.worker_distribution = [float(x) for x in params]
                elif args[0] == "worker_manager.dropout_time":
                    worker_manager.dropout_time = int(args[1])

                elif args[0] == "runtime":
                    self.runtime = int(args[1])
                elif args[0] == "output.time_stamp":
                    self.time_stamp = int(args[1])
                elif args[0] == "output.properties":
                    self.output_properties = args[1].split(',')
