import os
import subprocess


def check_noise(noise_mode, strength_noise):
    if not noise_mode:
        return False
    elif noise_mode:
        if strength_noise:
            ret_str = ["-n", str(strength_noise[0])]
            return ret_str
    return "краш"


def check_increase(increase_mode, type_increase, increase_strength):
    inf_var = {
        "По величине:": "-s",
        "По высоте:": "-h",
        "По ширине:": "-w",
    }
    if not increase_mode:
        return False
    elif increase_mode:
        if type_increase:
            if increase_strength[0] != "0":
                ret_str = [inf_var.get(type_increase), str(increase_strength)]
                return ret_str
    return "краш"


def create_output(input_path):
    output_path = input_path + "[WIF]"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def run_wifu(input_path, path_to_wif_state, noise_mode, increase_mode, increase_strength, strength_noise, type_increase):
    args = [path_to_wif_state, "-i", input_path, "-o", create_output(input_path)]

    add_scale = check_increase(increase_mode, type_increase, increase_strength)
    if add_scale == False or add_scale == "краш":
        args.append("-s")
        args.append("1")
    else:
        args.append(add_scale[0])
        args.append(add_scale[1])

    add_noise = check_noise(noise_mode, strength_noise)
    if add_noise == False or add_noise == "краш":
        args.append("-n")
        args.append("0")
    else:
        args.append(add_noise[0])
        args.append(add_noise[1])

    try:
        # Запуск внешнего процесса
        print(subprocess.run(args, check=True))
        return "ЗАВАЙФЛЕНО"

    except subprocess.CalledProcessError as e:
        print(e)
        pass