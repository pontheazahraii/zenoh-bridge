import random

from pycdr2 import make_idl_struct
from pycdr2.types import array, int8, int32, sequence, uint8, uint32

ACTION_NAME = "fibonacci"
SEND_GOAL_KEY = f"{ACTION_NAME}/_action/send_goal"
CANCEL_GOAL_KEY = f"{ACTION_NAME}/_action/cancel_goal"
GET_RESULT_KEY = f"{ACTION_NAME}/_action/get_result"
FEEDBACK_KEY = f"{ACTION_NAME}/_action/feedback"

GoalId = array(uint8, 16)

FibonacciSendGoal = make_idl_struct(
    "FibonacciSendGoal",
    "example_interfaces::action::dds_::Fibonacci_SendGoal_Request_",
    {
        "goal_id": GoalId,
        "goal": int32,
    },
)

ActionSendGoalResponse = make_idl_struct(
    "ActionSendGoalResponse",
    "example_interfaces::action::dds_::Fibonacci_SendGoal_Response_",
    {
        "accept": bool,
        "sec": int32,
        "nanosec": uint32,
    },
)

ActionResultRequest = make_idl_struct(
    "ActionResultRequest",
    "example_interfaces::action::dds_::Fibonacci_GetResult_Request_",
    {
        "goal_id": GoalId,
    },
)

FibonacciResult = make_idl_struct(
    "FibonacciResult",
    "example_interfaces::action::dds_::Fibonacci_GetResult_Response_",
    {
        "status": int8,
        "sequence": sequence(int32),
    },
)

FibonacciFeedback = make_idl_struct(
    "FibonacciFeedback",
    "example_interfaces::action::dds_::Fibonacci_FeedbackMessage_",
    {
        "goal_id": GoalId,
        "sequence": sequence(int32),
    },
)

GoalInfo = make_idl_struct(
    "GoalInfo",
    "action_msgs::msg::dds_::GoalInfo_",
    {
        "goal_id": GoalId,
        "stamp_sec": int32,
        "stamp_nanosec": uint32,
    },
)

CancelGoalRequest = make_idl_struct(
    "CancelGoalRequest",
    "action_msgs::srv::dds_::CancelGoal_Request_",
    {
        "goal_info": GoalInfo,
    },
)

CancelGoalResponse = make_idl_struct(
    "CancelGoalResponse",
    "action_msgs::srv::dds_::CancelGoal_Response_",
    {
        "return_code": int8,
        "goals_canceling": sequence(GoalInfo),
    },
)


def new_goal_id() -> GoalId:
    return bytes(random.randrange(256) for _ in range(16))


def fibonacci_sequence(order: int) -> list[int]:
    if order <= 0:
        return [0]
    if order == 1:
        return [0, 1]

    sequence = [0, 1]
    while len(sequence) <= order:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def feedback_sequence(order: int) -> list[int]:
    sequence = fibonacci_sequence(order)
    if len(sequence) <= 1:
        return sequence
    return sequence[:-1]
