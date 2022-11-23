import argparse
from os import path
import json
from . import mip
from . import reports


def _main():

    # Configure the command line argument parser
    parser = argparse.ArgumentParser(prog="escheduling", description="Assignment and Scheduling of Work Evaluation Commissions through Optimization Methods.")
    parser.add_argument('--output-dir', dest='output', type=str, default='.', help='Path to the directory to write the output files')
    parser.add_argument('input', metavar="FILE", type=str, help='Input file')
    args = parser.parse_args()

    # Load input data and solve the scheduling problem
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
        schedule = mip.solve(data)

    # Export schedule file
    schedule_template = path.join('templates', 'schedule-template.docx')
    schedule_output = path.join(args.output, 'schedule.docx')
    reports.schedule_to_doc(schedule_output, schedule_template, data, schedule)

    count = [0 for _ in range(0, len(data['evaluators']))]
    for entry in schedule:
        for j in entry['evaluators']:
            count[j] = count[j] + 1

    for j in range(0, len(data['evaluators'])):
        print('{}: {}'.format(data['evaluators'][j]['name'], count[j]))


if __name__ == "__main__":
    _main()
