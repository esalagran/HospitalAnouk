import argparse
import os

from main import find_result


def convert_file_to_dict(path):
    file_dict = {}
    with open(path, "r") as open_file:
        for line in open_file:
            split_line = line.split(": ")
            file_dict[split_line[0]] = split_line[1]
    return file_dict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", default="data/Exemplars/data")
    parser.add_argument("--save_path", default="data/Exemplars/solutions")
    parser.add_argument("--minimum_quality", default="data/calidad_minima_all_ejemplares.txt")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = parse_args()
    correct = 0
    passes_quality = 0
    minimum_quality_file = convert_file_to_dict(args.minimum_quality)
    for exemplar_txt in os.scandir(args.input_path):
        # if not os.path.isfile(exemplar_txt):
        #     continue
        if exemplar_txt.name == "ejemplar_p.txt":
            continue
        save_path = os.path.join(args.save_path, "sol_" + exemplar_txt.name)
        try:
            solution_cost = find_result(exemplar_txt.path, save_path)[0]
            if solution_cost >= float(minimum_quality_file[exemplar_txt.name]):
                passes_quality += 1

            print(
                f"{exemplar_txt.name} --> "
                f"solution_cost: {solution_cost} "
                f"acceptable cost: {minimum_quality_file[exemplar_txt.name]}"
            )
            correct += 1
        except Exception as e:
            print(f"{exemplar_txt.name}: {e}")

    print(f"Correct answers: {correct}")
    print(f"Number of accepted solutions: {passes_quality}")
