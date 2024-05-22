import os


def set_directories(base_path):

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    trial_dirs = [directory for directory in os.listdir(
        base_path) if os.path.isdir(os.path.join(base_path, directory))]
    trial_nums = sorted([int(directory[-1])
                        for directory in trial_dirs if directory.startswith("run") and directory[-1].isdigit()])
    next_trial_num = trial_nums[-1] + 1 if trial_nums else 1
    new_trial_path = os.path.join(base_path, f"run{next_trial_num}")

    os.makedirs(new_trial_path)
    return new_trial_path


def setup_dirs():

    home_folder = os.path.dirname(os.path.abspath(__file__))

    chkpt_path = os.path.join(home_folder, 'chkpts')
    chkpt_path = set_directories(chkpt_path)

    figure_path = os.path.join(home_folder, 'figures')
    figure_path = set_directories(figure_path)

    return chkpt_path, figure_path
