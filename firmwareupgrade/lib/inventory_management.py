from nornir.core.task import Task, Result
import os,sys
from config import settings


# WRITING THE NORNIR TASKS
def check_group_assignment(task: Task) -> Result:
    """
    check each host has only ONE group assigned.
    """
    if len(task.host.groups) > 1 or len(task.host.groups) == 0:
        return Result(
            host=task.host,
            result = f"ASSIGN ONE GROUP FOR {task.host.hostname}!!",
            failed = True
        )
    if len(task.host.groups) == 1:
        return Result(
            host=task.host,
            result = f"GROUPS CHECKED FOR {task.host.hostname}!!",
            failed = False
        )


def check_model_supported(task: Task) -> Result:
    """
    Compare each group to the class mappings in upgrade engine
    """
    for i in task.host.groups:
        if str(i) in settings['upgrade-mappings']:
            return Result(
                host=task.host,
                result=f"FOUND SUPPORT FOR {str(i).upper()}",
                failed=False
            )
        else:
            return Result(
                host=task.host,
                result=f"COULD NOT FIND SUPPORT FOR {str(i).upper()}",
                failed=True
            )


def check_firmware(task: Task) -> Result:
    """
    Check that the firmware for each host exists
    """
    firmware_exists = {}
    failed = False
    for i in task.host['upgrade_path']:
        firmware_exists.update({f"{i['firmware_location']}{i['firmware_file_name']}": os.path.exists(f"{i['firmware_location']}{i['firmware_file_name']}")})

    for i in task.host['upgrade_path']:
        if firmware_exists[(i['firmware_location']+i['firmware_file_name'])] == False:
            failed = True
    return Result(
        host=task.host,
        result=f"{task.host.hostname}: {firmware_exists}",
        failed=failed
    )


def full_checks(task: Task):
    firmware_result = task.run(
        name="CHECKING FIRMWARE EXISTS...",
        task=check_firmware,
    )
    group_result = task.run(
        name="CHECKING GROUP ASSIGNMENT...",
        task=check_group_assignment
    )
    supported_result = task.run(
        name="CHECKING MODEL SUPPORTED...",
        task=check_model_supported
    )