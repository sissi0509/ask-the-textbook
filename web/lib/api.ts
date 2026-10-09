// Talks to the FastAPI backend (src/tutor/api.py).
// The backend address is configuration: set NEXT_PUBLIC_API_URL in .env.local
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Source = { n: number; label: string; ref: string };
export type Passage = { n: number; label: string; content: string };
export type AnswerResult = {
  text: string;
  sources: Source[];
  invalid_citations: number[];
  grounded: boolean; // passed the citation gate (cites at least one real passage)
  attempts: number;
  passages: Passage[];
  input_tokens: number;
  output_tokens: number;
  cost_usd: number;
};

type StreamEvent =
  | { type: "text"; text: string }
  | { type: "retry"; reason: string }
  | { type: "done"; answer: AnswerResult }
  | { type: "error"; message: string };

/**
 * POST a question and read the answer as it streams.
 * The backend sends NDJSON: one JSON object per line ("text" pieces, then "done").
 * Calls onText with each new piece; resolves with the finished answer.
 * Calls onRetry when an attempt failed the citation gate: drop the text so far,
 * a new attempt streams next.
 */
export async function streamAnswer(
  path: "/ask" | "/ask/direct",
  question: string,
  onText: (piece: string) => void,
  onRetry: () => void = () => {},
): Promise<AnswerResult> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!response.ok || !response.body) {
    throw new Error(`The server answered ${response.status}.`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // A chunk can end mid-line, so keep the unfinished last line for next time.
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      if (!line.trim()) continue;
      const event = JSON.parse(line) as StreamEvent;
      if (event.type === "text") onText(event.text);
      else if (event.type === "retry") onRetry();
      else if (event.type === "done") return event.answer;
      else throw new Error(event.message);
    }
  }
  throw new Error("The answer stopped before it finished.");
}
