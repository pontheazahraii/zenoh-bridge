import sys

from pycdr2 import make_idl_struct
import zenoh

KEY = "add_two_ints"

AddTwoIntsRequest = make_idl_struct(
    "AddTwoIntsRequest",
    "example_interfaces::srv::dds_::AddTwoInts_Request_",
    {
        "a": int,
        "b": int,
    },
)

AddTwoIntsResponse = make_idl_struct(
    "AddTwoIntsResponse",
    "example_interfaces::srv::dds_::AddTwoInts_Response_",
    {
        "sum": int,
    },
)


def parse_args() -> tuple[int, int]:
    if len(sys.argv) == 3:
        return int(sys.argv[1]), int(sys.argv[2])
    return 2, 3


def encode_add_two_ints_request(a: int, b: int) -> bytes:
    return AddTwoIntsRequest(a=a, b=b).serialize()


def decode_add_two_ints_response(payload: bytes) -> int:
    return AddTwoIntsResponse.deserialize(payload).sum


def main() -> None:
    a, b = parse_args()
    payload = encode_add_two_ints_request(a, b)

    with zenoh.open(zenoh.Config()) as session:
        replies = session.get(
            KEY,
            payload=payload,
            encoding=zenoh.Encoding.APPLICATION_CDR,
            timeout=15.0,
        )

        for reply in replies:
            if reply.err is not None:
                raise RuntimeError(
                    "Query failed (bridge/server not ready or incompatible DDS settings): "
                    + reply.err.payload.to_string()
                )

            sample = reply.ok
            if sample is None:
                continue

            total = decode_add_two_ints_response(sample.payload.to_bytes())
            print(f"Response: {a} + {b} = {total}")
            return

    raise RuntimeError("No reply received")


if __name__ == "__main__":
    main()
