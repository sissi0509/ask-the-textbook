# Ask the Textbook: web chat

Next.js frontend for the FastAPI backend in `../src/tutor/api.py`.

```bash
cp .env.example .env.local   # NEXT_PUBLIC_API_URL, defaults to http://localhost:8000
npm install
npm run dev                  # http://localhost:3100
```

- `app/page.tsx`: the chat page (example questions, compare toggle, input)
- `components/AnswerCard.tsx`: one answer (streamed Markdown, sources, retrieved passages, cost)
- `lib/api.ts`: reads the backend's NDJSON stream
