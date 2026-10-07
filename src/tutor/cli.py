"""Ask the textbook a question from the terminal.

Run:  uv run python -m tutor.cli "Why do I lean back when the bus starts?"
      add --passages to also print the retrieved passages
"""

import argparse

from tutor.answer import Answer, label, stream_answer
from tutor.config import DEFAULT_METHOD
from tutor.db import connect
from tutor.retrieve import METHODS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--method", default=DEFAULT_METHOD, choices=list(METHODS))
    parser.add_argument("--passages", action="store_true", help="print the retrieved passages")
    args = parser.parse_args()

    with connect() as conn:
        answer = None
        for piece in stream_answer(conn, args.question, method=args.method):
            if isinstance(piece, Answer):
                answer = piece
            else:
                print(piece, end="", flush=True)
    print("\n")

    print("Sources")
    for n in answer.cited:
        if 1 <= n <= len(answer.passages):
            print(f"  [{n}] {label(answer.passages[n - 1])}")
    if answer.invalid:
        print(f"  ⚠ cited passages that weren't provided: {answer.invalid}")
    if not answer.cited:
        print("  ⚠ the answer cites no passages")
    if args.passages:
        print("\nRetrieved passages")
        for i, hit in enumerate(answer.passages, start=1):
            print(f"\n[{i}] {label(hit)}\n{hit.content}")
    print(f"\n({answer.input_tokens} in / {answer.output_tokens} out tokens, ~${answer.cost_usd:.3f})")


if __name__ == "__main__":
    main()
