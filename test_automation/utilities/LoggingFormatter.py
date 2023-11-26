import types
from inspect import stack
from test_automation.utilities import log
from test_automation.utilities.log import logger, LogColor
from datetime import datetime

STANDARD_WIDTH = 80


def format_test_func_start(function_name, step_count):
    ret = " Testing {} - {} STEPS TO VERIFY ".format(function_name, step_count)
    return ret.center(STANDARD_WIDTH, "-")


def format_step(index, description):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    ret = " Step {}: {} ".format(index, description)
    return f":: {current_time} :: >>>" + ret


def format_verification(index):
    ret = " CHECKING STEP #{} ".format(index)
    return ret.center(STANDARD_WIDTH, "*")


def fancy_center(string, width, left, right, color=LogColor.BLACK):
    padding_width = width - len(string)
    if padding_width <= 0:
        return string
    left_padding_width = padding_width // 2
    right_padding_width = padding_width - left_padding_width
    message = left * left_padding_width + string + right * right_padding_width
    return color.apply(message)


def format_test_case_start(test_case_name):
    ret = f" {test_case_name} "
    return fancy_center(ret, STANDARD_WIDTH, ">", "<")


def format_test_case_end(test_case_name):
    ret = "{} ".format(test_case_name)
    return ret.center(STANDARD_WIDTH, "-")


def format_step_verification(index, msg):
    ret = " >>> Step {}: Verification for {} --- PASSED ".format(index, msg)
    return ret.center(STANDARD_WIDTH, "*")


def _log_step(self, index, description):
    self.info(format_step(index, description))


def _log_test_case_start(self, test_case_name=None):
    if test_case_name is None:
        test_case_name = stack()[1].function
        print("calling function is: {!r}".format(test_case_name))
    self.debug(format_test_case_start(test_case_name))


def _log_test_case_end(self, test_case_name=None):
    self.info("")
    self.info(format_test_case_end(test_case_name))


def _log_info_step_verification(self, index, msg):
    if index is not None:
        self.info(format_step_verification(index, msg))


logger.debug_test_case_start = types.MethodType(_log_test_case_start, logger)
logger.info_step = types.MethodType(_log_step, logger)
logger.info_step_verification = types.MethodType(_log_info_step_verification, logger)
logger.info_test_case_end = types.MethodType(_log_test_case_end, logger)
