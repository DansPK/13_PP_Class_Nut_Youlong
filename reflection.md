# Reflection

**What worked well:** The recursive character splitter (paragraph → line → sentence →
word, with overlap) held up well against the short, well-structured helpdesk documents —
in-scope test questions (PIN reset, VPN setup, printer jam, Webex setup) consistently
retrieved the correct source chunk with high cosine similarity (0.65–0.92) and produced
accurate, cited answers. The groundedness guardrail also worked largely as intended: an
off-topic question ("What is the CEO's home address?") correctly triggered the "I don't
have enough information" fallback instead of a hallucinated answer.

**What was harder than expected:** Tuning `SIMILARITY_THRESHOLD` turned out to be more
delicate than a single number should be. Scores for genuinely irrelevant chunks
(~0.45–0.57) overlapped with scores for weak-but-real matches, so a low threshold let
unrelated chunks slip into the context window even on the off-topic test question. Worse,
the model then cited those irrelevant sources *alongside* the "I don't have enough
information" refusal, which looked contradictory. Fixing it took two changes together —
raising the threshold (0.4 → 0.55) to keep noisy chunks out, and rewriting the system
prompt to require the fallback reply verbatim with no citations — since either fix alone
left a gap the other one covered.

**Future improvement — query rewriting:** Right now the raw user question is embedded and
searched as-is, so short or ambiguous follow-ups ("what about the tablet one?") retrieve
poorly. Adding a query-rewriting step — using the chat history to reformulate the question
into a self-contained, retrieval-friendly query before embedding it — would likely improve
recall on multi-turn conversations without touching the chunking or generation stages at
all.
