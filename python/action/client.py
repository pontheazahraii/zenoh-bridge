import sys
import time

import zenoh

from action_types import (
    ACTION_NAME,
    FEEDBACK_KEY,
    GET_RESULT_KEY,
    SEND_GOAL_KEY,
    ActionResultRequest,
    ActionSendGoalResponse,
    FibonacciFeedback,
    FibonacciResult,
    FibonacciSendGoal,
    new_goal_id,
)


def parse_args() -> int:
    if len(sys.argv) == 2:
        return int(sys.argv[1])
    return 5


def main() -> None:
    order = parse_args()
    goal_id = new_goal_id()

    with zenoh.open(zenoh.Config()) as session:
        feedback_subscriber = session.declare_subscriber(FEEDBACK_KEY)

        send_goal_request = FibonacciSendGoal(goal_id=goal_id, goal=order).serialize()
        send_goal_replies = session.get(
            SEND_GOAL_KEY,
            payload=send_goal_request,
            encoding=zenoh.Encoding.APPLICATION_CDR,
            timeout=15.0,
        )

        accepted = False
        for reply in send_goal_replies:
            if reply.err is not None:
                raise RuntimeError(reply.err.payload.to_string())

            sample = reply.ok
            if sample is None:
                continue

            response = ActionSendGoalResponse.deserialize(sample.payload.to_bytes())
            accepted = response.accept
            print(f"Goal accepted: {response.accept}")
            break

        if not accepted:
            raise RuntimeError("Goal was not accepted")

        deadline = time.time() + 15.0
        while time.time() < deadline:
            sample = feedback_subscriber.try_recv()
            if sample is None:
                time.sleep(0.1)
                continue

            feedback = FibonacciFeedback.deserialize(sample.payload.to_bytes())
            if feedback.goal_id != goal_id:
                continue

            print(f"Feedback: {feedback.sequence}")
            break
        else:
            raise RuntimeError("Timed out waiting for action feedback")

        get_result_request = ActionResultRequest(goal_id=goal_id).serialize()
        result_replies = session.get(
            GET_RESULT_KEY,
            payload=get_result_request,
            encoding=zenoh.Encoding.APPLICATION_CDR,
            timeout=15.0,
        )

        for reply in result_replies:
            if reply.err is not None:
                raise RuntimeError(reply.err.payload.to_string())

            sample = reply.ok
            if sample is None:
                continue

            result = FibonacciResult.deserialize(sample.payload.to_bytes())
            print(f"Result status: {result.status}")
            print(f"Result sequence: {result.sequence}")
            return

    raise RuntimeError(f"No result received for action {ACTION_NAME}")


if __name__ == "__main__":
    main()
