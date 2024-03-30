#!/usr/bin/env python
from maf_comparator.crew import MafComparatorCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    MafComparatorCrew().crew().kickoff(inputs=inputs)