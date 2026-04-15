import time

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


def decode_add_two_ints_request(payload: bytes) -> tuple[int, int]:
    request = AddTwoIntsRequest.deserialize(payload)
    return request.a, request.b


def encode_add_two_ints_response(total: int) -> bytes:
    return AddTwoIntsResponse(sum=total).serialize()


def on_query(query: zenoh.Query) -> None:
    a, b = decode_add_two_ints_request(query.payload.to_bytes())
    total = a + b
    payload = encode_add_two_ints_response(total)

    print(f"Handled query: {a} + {b} = {total}")
    query.reply(KEY, payload, encoding=zenoh.Encoding.APPLICATION_CDR)


def main() -> None:
    with zenoh.open(zenoh.Config()) as session:
        print(f"Zenoh queryable ready on {KEY}")

        with session.declare_queryable(KEY, on_query):
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping Zenoh service server...")


if __name__ == "__main__":
    main()
