"""

 OMRChecker

 Author: Udayraj Deshmukh
 Github: https://github.com/Udayraj123

"""
import os
from csv import QUOTE_NONNUMERIC
from pathlib import Path
from time import time

import cv2
import pandas as pd
from rich.table import Table

from src import constants
from src.defaults import CONFIG_DEFAULTS
from src.evaluation import EvaluationConfig, evaluate_concatenated_response
from src.logger import console, logger
from src.template import Template
from src.utils.file import Paths, setup_dirs_for_paths, setup_outputs_for_template
from src.utils.image import ImageUtils
from src.utils.interaction import InteractionUtils, Stats
from src.utils.parsing import get_concatenated_response, open_config_with_defaults
import pickle

# Load processors
STATS = Stats()


def entry_point(omr_file: Path, basepath: str):
    root_dir = Path(basepath)
    curr_dir = Path(basepath)
    local_config_path = curr_dir.joinpath(constants.CONFIG_FILENAME)
    tuning_config = open_config_with_defaults(local_config_path)
    local_template_path = curr_dir.joinpath(constants.TEMPLATE_FILENAME)
    template = Template(
        local_template_path,
        tuning_config,
    )
    output_dir = Path("outputs", curr_dir.relative_to(root_dir))
    paths = Paths(output_dir)
    setup_dirs_for_paths(paths)
    outputs_namespace = setup_outputs_for_template(paths, template)
    evaluation_config = None
    omr_files = [omr_file]
    return process_files(
        omr_files,
        template,
        tuning_config,
        evaluation_config,
        outputs_namespace,)

def process_files(
    omr_files,
    template,
    tuning_config,
    evaluation_config,
    outputs_namespace,
):
    start_time = int(time())
    files_counter = 0
    STATS.files_not_moved = 0

    for file_path in omr_files:
        files_counter += 1
        file_name = file_path.name

        in_omr = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
        template.image_instance_ops.reset_all_save_img()
        template.image_instance_ops.append_save_img(1, in_omr)
        in_omr = template.image_instance_ops.apply_preprocessors(
            file_path, in_omr, template
        )
        # uniquify
        file_id = str(file_name)
        save_dir = outputs_namespace.paths.save_marked_dir
        (
            response_dict,
            final_marked,
            multi_marked,
            _,
        ) = template.image_instance_ops.read_omr_response(
            template, image=in_omr, name=file_id, save_dir=save_dir
        )
        omr_response = get_concatenated_response(response_dict, template)
        score = 0
        resp_array = []
        for k in template.output_columns:
            resp_array.append(omr_response[k])
        # print(pickle.dumps(resp_array))
        return resp_array
