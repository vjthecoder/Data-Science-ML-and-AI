import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 02. Chunking Strategies

        ## Theory

        **Level 1 (10-year-old):** A whole book is too big to hand the AI at once. So we cut it
        into bite-sized pieces. Cut too big and each piece is messy; cut too small and pieces lose
        their meaning. Finding the right size is the trick.

        **Level 2 (College Student):** Chunking splits documents into retrievable units before
        embedding. Strategies: **fixed-size** (every N characters/tokens), **fixed-size with
        overlap** (carry the last X chars into the next chunk to preserve context across
        boundaries), **recursive** (split on natural boundaries — paragraphs, then sentences),
        and **semantic** (split where the topic shifts). Chunk size trades precision (small =
        focused) against context (large = self-contained).

        **Level 3 (Industry Professional):** Chunking is one of the highest-leverage RAG knobs.
        Choose chunk size based on the embedding model's optimal input length, the document
        structure (code, prose, tables), and the question type (fact lookup vs synthesis). Always
        keep metadata (source, page, heading) per chunk for filtering and citations. Overlap
        (10-20%) reduces boundary loss but increases storage and duplicate hits. For structured
        docs, split on headings/markdown structure rather than blind character counts.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Fixed-size (size=100, overlap=0):
          [0-100][100-200][200-300]      ← may cut sentences in half

        Fixed-size with overlap (size=100, overlap=20):
          [0-100][80-180][160-260]       ← each chunk repeats last 20 chars of prior

        Recursive:
          split on "\n\n" → too big? split on "\n" → too big? split on ". " → words

        Too small: "The termination" | "notice is 30"   ← meaning lost
        Too big:   <entire 5-page section>               ← retrieval imprecise
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: fixed-size chunking with overlap (pure Python, no deps)
    def chunk_fixed(text, size=200, overlap=40):
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            start = end - overlap          # step back by overlap
            if start <= 0:
                break
        return chunks

    sample = ("Retrieval-augmented generation grounds LLM answers in retrieved documents. "
              "Chunking splits documents into retrievable units. Chunk size trades precision "
              "against context. Overlap preserves meaning across chunk boundaries.")
    chunks = chunk_fixed(sample, size=120, overlap=30)
    for i, c in enumerate(chunks):
        print(f"[{i}] ({len(c)} chars) {c!r}")
    return chunk_fixed, chunks, sample


@app.cell
def __():
    # Recursive chunking: prefer natural boundaries before falling back to hard splits
    def chunk_recursive(text, max_size=200, seps=("\n\n", "\n", ". ", " ")):
        if len(text) <= max_size:
            return [text]
        for sep in seps:
            if sep in text:
                parts, cur, out = text.split(sep), "", []
                for p in parts:
                    piece = p + sep
                    if len(cur) + len(piece) <= max_size:
                        cur += piece
                    else:
                        if cur:
                            out.append(cur.strip())
                        cur = piece
                if cur:
                    out.append(cur.strip())
                # recurse on any still-too-large chunk
                result = []
                for o in out:
                    result.extend(chunk_recursive(o, max_size, seps) if len(o) > max_size else [o])
                return result
        return [text[i:i+max_size] for i in range(0, len(text), max_size)]

    doc = ("# Intro\n\nRAG has two phases.\n\n# Indexing\n\nChunk, embed, store. "
           "This section is intentionally long to force a split into multiple pieces "
           "so we can see recursive behavior in action across sentence boundaries.")
    for i, c in enumerate(chunk_recursive(doc, max_size=80)):
        print(f"[{i}] {c!r}")
    return chunk_recursive, doc


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        For a markdown knowledge base, splitting on headings keeps each chunk topically coherent
        and lets you store the heading path as metadata (`{"section": "Billing > Refunds"}`). In
        production you'd use a library:

        ```python
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(document_text)
        ```

        ## Coding Exercise

        1. Chunk a 1000-word document with three configs: (size=200, overlap=0),
           (size=200, overlap=40), (size=500, overlap=50). Count the chunks each produces.
        2. For a query whose answer spans a sentence boundary, show that overlap retrieves the
           full answer where no-overlap splits it.
        3. Write a chunker that splits a markdown doc on `#`/`##` headings and attaches the
           heading as metadata to each chunk.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week04_assignments.md` — Assignment 2.

        ## Interview Questions
        See `../../interview-prep/week04_rag_questions.md` — Section: Chunking.

        ## Industry Use Cases
        - Heading-aware chunking for documentation sites
        - Code-aware chunking (split on functions/classes) for code search
        - Table/row chunking for spreadsheet/CSV retrieval

        ## Common Mistakes
        - Chunks too large (imprecise retrieval) or too small (lost meaning)
        - Blind character splits that cut sentences/tables mid-way
        - Dropping metadata, losing citation ability

        ## Best Practices
        - Match chunk size to embedding model + content structure
        - Use 10-20% overlap for prose; split on structure for docs/code
        - Keep source/heading/page metadata on every chunk

        ## Further Reading
        - LangChain text splitters documentation
        - "Semantic chunking" approaches and benchmarks
        """
    )
    return


if __name__ == "__main__":
    app.run()
