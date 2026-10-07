"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import AnswerCard, { type AnswerState } from "@/components/AnswerCard";
import { streamAnswer } from "@/lib/api";

type Turn = { question: string; answers: AnswerState[] };

const EXAMPLES = [
  "Why do I lean back when the bus suddenly starts?",
  "Why does a spinning ice skater speed up when she pulls her arms in?",
  "Why do we see a rainbow after it rains?",
  "What is the origin of redshift: the Doppler effect or relativity?",
];

export default function Home() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [compare, setCompare] = useState(false);
  const [busy, setBusy] = useState(false);
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns]);

  // Update one answer of the latest turn without touching the rest of the chat.
  function updateAnswer(index: number, change: (a: AnswerState) => AnswerState) {
    setTurns((prev) => {
      const last = prev[prev.length - 1];
      const answers = last.answers.map((a, i) => (i === index ? change(a) : a));
      return [...prev.slice(0, -1), { ...last, answers }];
    });
  }

  async function ask(question: string) {
    const q = question.trim();
    if (!q || busy) return;
    setInput("");
    setBusy(true);
    const kinds: AnswerState["kind"][] = compare ? ["textbook", "memory"] : ["textbook"];
    setTurns((prev) => [...prev, { question: q, answers: kinds.map((kind) => ({ kind, text: "" })) }]);

    // Each question is answered on its own; earlier turns aren't sent to the model.
    await Promise.all(
      kinds.map(async (kind, index) => {
        try {
          const result = await streamAnswer(kind === "textbook" ? "/ask" : "/ask/direct", q, (piece) =>
            updateAnswer(index, (a) => ({ ...a, text: a.text + piece })),
          );
          updateAnswer(index, (a) => ({ ...a, text: result.text, result }));
        } catch (err) {
          const message = err instanceof Error ? err.message : "Something went wrong.";
          updateAnswer(index, (a) => ({ ...a, error: `Couldn't get an answer: ${message}` }));
        }
      }),
    );
    setBusy(false);
  }

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    ask(input);
  }

  return (
    <div className="flex min-h-screen flex-col bg-stone-100 text-stone-900 dark:bg-stone-950 dark:text-stone-100">
      <header className="sticky top-0 z-10 border-b border-stone-200 bg-stone-100/90 backdrop-blur dark:border-stone-800 dark:bg-stone-950/90">
        <div className="mx-auto flex max-w-4xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <div>
            <h1 className="text-lg font-semibold">📘 Ask the Textbook</h1>
            <p className="text-xs text-stone-500">A grounded physics tutor · OpenStax University Physics, Vols. 1–3</p>
          </div>
          <label className="flex cursor-pointer items-center gap-2 text-sm text-stone-600 dark:text-stone-300">
            <input type="checkbox" checked={compare} onChange={(e) => setCompare(e.target.checked)} className="h-4 w-4 accent-amber-600" />
            Compare with memory only
          </label>
        </div>
      </header>

      <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-6">
        {turns.length === 0 ? (
          <div className="mt-10 text-center">
            <p className="mb-2 text-2xl font-semibold">Ask a physics question in your own words.</p>
            <p className="mb-6 text-sm text-stone-500">Every answer cites the textbook sections it comes from.</p>
            <div className="mx-auto grid max-w-2xl gap-2 sm:grid-cols-2">
              {EXAMPLES.map((example) => (
                <button
                  key={example}
                  onClick={() => ask(example)}
                  className="rounded-xl border border-stone-200 bg-white p-3 text-left text-sm hover:border-amber-400 hover:bg-amber-50 dark:border-stone-800 dark:bg-stone-900 dark:hover:bg-stone-800"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            {turns.map((turn, t) => (
              <section key={t} className="space-y-3">
                <div className="flex justify-end">
                  <p className="max-w-[80%] rounded-2xl bg-amber-600 px-4 py-2 text-white">{turn.question}</p>
                </div>
                <div className={turn.answers.length > 1 ? "grid gap-4 md:grid-cols-2" : ""}>
                  {turn.answers.map((answer, i) => (
                    <AnswerCard key={i} answer={answer} showTitle={turn.answers.length > 1} />
                  ))}
                </div>
              </section>
            ))}
            <div ref={bottom} />
          </div>
        )}
      </main>

      <footer className="sticky bottom-0 border-t border-stone-200 bg-stone-100/95 dark:border-stone-800 dark:bg-stone-950/95">
        <form onSubmit={onSubmit} className="mx-auto flex max-w-4xl gap-2 px-4 py-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                ask(input);
              }
            }}
            rows={1}
            placeholder="Ask a physics question…"
            aria-label="Your question"
            className="flex-1 resize-none rounded-xl border border-stone-300 bg-white px-4 py-3 text-sm focus:border-amber-500 focus:outline-none dark:border-stone-700 dark:bg-stone-900"
          />
          <button
            type="submit"
            disabled={busy || !input.trim()}
            className="rounded-xl bg-amber-600 px-5 text-sm font-medium text-white hover:bg-amber-700 disabled:opacity-40"
          >
            {busy ? "Thinking…" : "Ask"}
          </button>
        </form>
      </footer>
    </div>
  );
}
