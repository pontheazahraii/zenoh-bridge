import time

import zenoh

from action_types import (
    ACTION_NAME,
    CANCEL_GOAL_KEY,
    FEEDBACK_KEY,
    FibonacciSendGoal,
    GET_RESULT_KEY,
    SEND_GOAL_KEY,
    ActionResultRequest,
    ActionSendGoalResponse,
    CancelGoalRequest,
    CancelGoalResponse,
    FibonacciFeedback,
    FibonacciResult,
    feedback_sequence,
    fibonacci_sequence,
)

GOAL_STATUS_SUCCEEDED = 4
CANCEL_RESPONSE_NONE = 0


class ActionServerState:
    def __init__(self) -> None:
        self.results: dict[tuple[int, ...], list[int]] = {}

    def accept_goal(self, goal_id: list[int], order: int) -> None:
        self.results[tuple(goal_id)] = fibonacci_sequence(order)

    def get_result(self, goal_id: list[int]) -> list[int] | None:
        return self.results.get(tuple(goal_id))


def main() -> None:
    state = ActionServerState()

    with zenoh.open(zenoh.Config()) as session:
        feedback_publisher = session.declare_publisher(
            FEEDBACK_KEY,
            encoding=zenoh.Encoding.APPLICATION_CDR,
        )

        def on_send_goal(query: zenoh.Query) -> None:
            goal_request = FibonacciSendGoal.deserialize(query.payload.to_bytes())
            state.accept_goal(goal_request.goal_id, goal_request.goal)

            feedback = FibonacciFeedback(
                goal_id=goal_request.goal_id,
                sequence=feedback_sequence(goal_request.goal),
            ).serialize()
            feedback_publisher.put(feedback)

            response = ActionSendGoalResponse(
                accept=True,
                sec=0,
                nanosec=0,
            ).serialize()

            print(f"Accepted goal: order={goal_request.goal}")
            query.reply(SEND_GOAL_KEY, response, encoding=zenoh.Encoding.APPLICATION_CDR)

        def on_get_result(query: zenoh.Query) -> None:
            request = ActionResultRequest.deserialize(query.payload.to_bytes())
            sequence = state.get_result(request.goal_id)
            if sequence is None:
                raise RuntimeError(f"Unknown goal id: {request.goal_id}")

            response = FibonacciResult(
                status=GOAL_STATUS_SUCCEEDED,
                sequence=sequence,
            ).serialize()

            print(f"Returned result: {sequence}")
            query.reply(GET_RESULT_KEY, response, encoding=zenoh.Encoding.APPLICATION_CDR)

        def on_cancel_goal(query: zenoh.Query) -> None:
            request = CancelGoalRequest.deserialize(query.payload.to_bytes())
            response = CancelGoalResponse(
                return_code=CANCEL_RESPONSE_NONE,
                goals_canceling=[],
            ).serialize()

            print("Cancel requested")
            query.reply(
                CANCEL_GOAL_KEY,
                response,
                encoding=zenoh.Encoding.APPLICATION_CDR,
            )

        print(f"Zenoh action server ready on {ACTION_NAME}")

        with session.declare_queryable(SEND_GOAL_KEY, on_send_goal):
            with session.declare_queryable(CANCEL_GOAL_KEY, on_cancel_goal):
                with session.declare_queryable(GET_RESULT_KEY, on_get_result):
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\nStopping Zenoh action server...")


if __name__ == "__main__":
    main()
