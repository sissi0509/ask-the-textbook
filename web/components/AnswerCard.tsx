import ReactMarkdown from "react-markdown";
import type { AnswerResult } from "@/lib/api";

export type AnswerState = {
  kind: "textbook" | "memory";
  text: string;
  result?: AnswerResult;
  error?: string;
};

const TITLES = {
  textbook: "📘 From the textbook",
  memory: "🧠 From memory only (no retrieval)",
};

export default function AnswerCard({ answer, showTitle }: { answer: AnswerState; showTitle: boolean }) {
  const { kind, text, result, error } = answer;
  const streaming = !result && !error;

  return (
    <div
      className={`rounded-2xl border p-5 shadow-sm ${
        kind === "textbook"
          ? "border-amber-200 bg-white dark:border-amber-900/60 dark:bg-stone-900"
          : "border-stone-200 bg-stone-50 dark:border-stone-700 dark:bg-stone-900/60"
      }`}
    >
      {showTitle && (
        <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-stone-500">{TITLES[kind]}</p>
      )}

      <div className="answer-markdown">
        <ReactMarkdown>{text + (streaming ? " ▍" : "")}</ReactMarkdown>
      </div>

      {error && <p className="mt-3 rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">{error}</p>}

      {result && kind === "textbook" && result.grounded === false && (
        <p className="mt-3 rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
          ⚠ Not grounded in the textbook: this answer failed the citation check after {result.attempts}{" "}
          {result.attempts === 1 ? "attempt" : "attempts"}. Treat it as unverified.
        </p>
      )}

      {result && kind === "textbook" && (
        <div className="mt-4 border-t border-stone-200 pt-3 dark:border-stone-700">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">Sources</p>
          {result.sources.length ? (
            <ul className="flex flex-wrap gap-2">
              {result.sources.map((s) => (
                <li key={s.n} className="rounded-full bg-amber-50 px-3 py-1 text-xs text-amber-900 dark:bg-amber-950 dark:text-amber-200">
                  [{s.n}] {s.label}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-stone-500">The answer cites no passages.</p>
          )}
          {result.invalid_citations.length > 0 && (
            <p className="mt-2 text-xs text-red-600">⚠ Cited passages that weren&apos;t provided: {result.invalid_citations.join(", ")}</p>
          )}
          <details className="mt-3 text-sm">
            <summary className="cursor-pointer text-stone-600 hover:text-stone-900 dark:text-stone-400 dark:hover:text-stone-100">
              Show the {result.passages.length} retrieved passages
            </summary>
            <ol className="mt-3 space-y-3">
              {result.passages.map((p) => (
                <li key={p.n} className="rounded-lg bg-stone-50 p-3 dark:bg-stone-800">
                  <p className="mb-1 text-xs font-semibold text-stone-600 dark:text-stone-300">[{p.n}] {p.label}</p>
                  <p className="whitespace-pre-line text-stone-700 dark:text-stone-300">{p.content}</p>
                </li>
              ))}
            </ol>
          </details>
        </div>
      )}

      {result && (
        <p className="mt-3 text-xs text-stone-400">
          {result.input_tokens.toLocaleString()} in / {result.output_tokens.toLocaleString()} out tokens · ~$
          {result.cost_usd.toFixed(3)}
          {result.attempts > 1 && ` · rewritten to fix citations (${result.attempts} attempts)`}
        </p>
      )}
    </div>
  );
}
