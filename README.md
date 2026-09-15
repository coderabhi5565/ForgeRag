# ForgeRAG 🔥

### Production AI Knowledge System

ForgeRAG is a production-oriented **Retrieval-Augmented Generation (RAG)** system built to explore and implement the engineering principles behind reliable AI applications.

The goal is not simply to build another "chat with your PDF" application.

ForgeRAG is designed as a hands-on AI engineering laboratory where retrieval, grounding, evaluation, and production quality are treated as first-class engineering problems.

---

## 🎯 What Are We Building?

ForgeRAG allows users to upload domain-specific documents and ask questions about them.

Instead of relying entirely on the LLM's internal knowledge, the system retrieves relevant information from the user's documents and uses that information to generate grounded answers with source citations.

The core pipeline is:

```text
Documents
    ↓
Document Processing
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Search
    +
BM25 Search
    ↓
Hybrid Retrieval
    ↓
Cross-Encoder Reranking
    ↓
Relevant Context
    ↓
LLM Generation
    ↓
Grounded Answer
    ↓
Citations
    ↓
Ragas Evaluation
    ↓
CI Quality Gate
```

---

# 🧠 Why ForgeRAG?

A basic RAG application can be built quickly:

```text
PDF → Embeddings → Vector DB → LLM
```

But production AI systems introduce much harder questions:

* What happens when semantic search misses an important keyword?
* How do we combine lexical and semantic retrieval?
* How many candidates should retrieval return?
* Why should we rerank retrieved documents?
* How do we prevent the LLM from inventing information?
* How do we enforce citations?
* How do we know whether retrieval is actually improving?
* How do we detect when a code change makes the RAG system worse?
* Can AI quality become part of CI/CD rather than manual inspection?

ForgeRAG is built to answer these questions through implementation and experimentation.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Client        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      API Layer      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Document Ingestion│            │    Query API     │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Text Extraction  │            │ Query Processing │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │     Chunking     │            │ Hybrid Retrieval │
          └────────┬─────────┘            └────────┬─────────┘
                   │                         ┌─────┴─────┐
                   ▼                         ▼           ▼
          ┌──────────────────┐          ┌────────┐   ┌────────┐
          │    Embeddings    │          │ Vector │   │  BM25  │
          └────────┬─────────┘          │ Search │   │ Search │
                   │                    └────┬───┘   └────┬───┘
                   ▼                         │            │
          ┌──────────────────┐               └─────┬──────┘
          │   Vector Store   │                     ▼
          └──────────────────┘              ┌───────────────┐
                                            │ Result Fusion │
                                            └───────┬───────┘
                                                    │
                                                    ▼
                                            ┌───────────────┐
                                            │ Cross-Encoder │
                                            │   Reranking   │
                                            └───────┬───────┘
                                                    │
                                                    ▼
                                            ┌───────────────┐
                                            │Context Builder│
                                            └───────┬───────┘
                                                    │
                                                    ▼
                                            ┌───────────────┐
                                            │      LLM      │
                                            └───────┬───────┘
                                                    │
                                                    ▼
                                            ┌───────────────┐
                                            │Answer +       │
                                            │Citations      │
                                            └───────────────┘
```

---

# 🔎 Retrieval Architecture

ForgeRAG intentionally uses two retrieval strategies.

### Semantic Retrieval

Documents are converted into embeddings and stored in a vector database.

```text
Query
 ↓
Embedding
 ↓
Vector Search
 ↓
Semantic Candidates
```

This allows the system to retrieve conceptually similar content even when exact words differ.

### Lexical Retrieval

BM25 provides keyword-oriented retrieval.

```text
Query
 ↓
BM25
 ↓
Lexical Candidates
```

This is particularly useful when exact terms, names, identifiers, technical terminology, or rare keywords matter.

### Hybrid Retrieval

The two candidate sets are combined using a result-fusion strategy.

```text
Vector Results
       +
BM25 Results
       ↓
Result Fusion
       ↓
Candidate Pool
```

The exact fusion strategy will be implemented and evaluated as part of the project.

---

# 🎯 Reranking

Initial retrieval is designed for **high recall**.

The retrieved candidates are then passed through a cross-encoder reranker.

```text
Query
 +
Candidate Document
        ↓
Cross Encoder
        ↓
Relevance Score
```

This creates a second-stage ranking process:

```text
Large Corpus
     ↓
Fast Retrieval
     ↓
Candidate Set
     ↓
More Accurate Reranking
     ↓
Final Context
```

The project will explicitly measure why and when reranking helps rather than treating it as a black-box component.

---

# 📚 Grounded Generation

The LLM should answer using retrieved document context rather than freely generating unsupported information.

The generation pipeline will therefore contain:

```text
Retrieved Context
      ↓
Context Construction
      ↓
LLM
      ↓
Answer
      ↓
Citation Validation
```

Each relevant chunk will preserve source metadata so that generated answers can reference the underlying document and location.

---

# 🧪 Evaluation

AI quality will be treated as an engineering concern.

ForgeRAG will use an evaluation dataset containing representative questions and expected/reference information.

The RAG pipeline will be evaluated using Ragas and relevant retrieval/generation metrics.

The evaluation flow is:

```text
Evaluation Dataset
       ↓
ForgeRAG Pipeline
       ↓
Generated Answers
       ↓
Ragas
       ↓
Quality Metrics
       ↓
Threshold Validation
```

The goal is to move from:

> "The answer looks good."

to:

> "The system meets measurable quality criteria."

---

# 🚦 CI Quality Gate

Evaluation will eventually run automatically in CI.

```text
Pull Request
     ↓
Run Tests
     ↓
Run RAG Evaluation
     ↓
Calculate Metrics
     ↓
Compare Against Thresholds
     ↓
 ┌─────────────┐
 │             │
PASS          FAIL
 │             │
 ▼             ▼
Continue      Block
```

This makes AI quality part of the software delivery process.

A change that improves code but significantly degrades retrieval or answer quality should be detectable before it reaches production.

---

# 🧩 Project Structure

```text
ForgeRAG/
│
├── app/
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   ├── models/
│   ├── services/
│   ├── config/
│   └── main.py
│
├── tests/
│
├── data/
│   ├── documents/
│   └── evaluation/
│
├── scripts/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The repository structure will evolve as the system grows. New abstractions and modules will be introduced when they solve a real engineering problem.

---

# 🛠️ Technology Direction

ForgeRAG is primarily implemented in Python.

The system is expected to use:

* Python
* FastAPI
* LLM API
* Embedding model
* Vector database
* BM25
* Cross-encoder reranking
* Ragas
* CI/CD

Specific implementation choices will be made according to the problem being solved rather than adding technologies purely for their names.

Frameworks such as LangChain or LangGraph will not be introduced unless they provide a genuine architectural or learning benefit.

---

# 🤖 Future Agentic Layer

Agentic functionality is intentionally not part of the initial core pipeline.

If the system later requires multi-step reasoning or external capabilities, it may evolve toward:

```text
User
 ↓
Agent
 ↓
Decision
 ↓
Tool Calling
 ↓
External Capability
 ↓
Observation
 ↓
Next Decision
```

MCP may subsequently be introduced where standardized tool/context integration provides a real architectural benefit.

The project will not add agents or MCP simply as resume keywords.

---

# 🧠 Learning Philosophy

ForgeRAG is simultaneously a production-style project and an AI engineering learning laboratory.

The primary goal is:

> **Deep understanding over project completion.**

When a new concept becomes necessary, the implementation pauses long enough to understand the underlying engineering problem.

The learning loop is:

```text
Understand
    ↓
Implement
    ↓
Break It
    ↓
Debug
    ↓
Improve
    ↓
Measure
    ↓
Continue
```

The project intentionally avoids hiding important concepts behind framework abstractions.

Whenever practical, the underlying mechanism will be understood before using a higher-level library.

---

# 📈 Engineering Principles

ForgeRAG follows several principles:

### 1. Measure AI quality

Manual inspection is useful, but insufficient.

### 2. Optimize retrieval before generation

A powerful LLM cannot reliably answer questions from context that retrieval failed to provide.

### 3. Prefer simple architecture

Abstractions are introduced when they solve real problems.

### 4. Understand the internals

Libraries accelerate implementation; they should not replace understanding.

### 5. Experiment deliberately

Retrieval strategies, chunking approaches, reranking, prompts, and thresholds should be evaluated rather than assumed to be optimal.

### 6. Keep the system replaceable

Core components should have clear boundaries so individual implementations can evolve.

### 7. Don't optimize for buzzwords

Every major technology in the final system should have a defensible reason for existing.

---

# 🚀 Project Status

**Status: Building from scratch**

Current phase:

```text
Phase 1
Document Ingestion
```

The system will be developed incrementally.

Major milestones:

* [ ] Project setup
* [ ] Document ingestion
* [ ] Text extraction
* [ ] Chunking
* [ ] Metadata model
* [ ] Embedding pipeline
* [ ] Vector storage
* [ ] BM25 retrieval
* [ ] Hybrid retrieval
* [ ] Result fusion
* [ ] Cross-encoder reranking
* [ ] Context construction
* [ ] LLM generation
* [ ] Citation enforcement
* [ ] RAG evaluation dataset
* [ ] Ragas evaluation
* [ ] CI quality gate
* [ ] Production hardening
* [ ] Agentic extension, if justified
* [ ] Tool calling, if justified
* [ ] MCP integration, if justified

---

# 🔥 Final Objective

ForgeRAG should result in more than a working application.

By the end of the project, the system should be understandable end-to-end:

```text
Document
   ↓
Chunk
   ↓
Embedding
   ↓
Index
   ↓
Retrieve
   ↓
Fuse
   ↓
Rerank
   ↓
Build Context
   ↓
Generate
   ↓
Cite
   ↓
Evaluate
   ↓
Gate
```

And every major arrow should be something the engineer can explain, debug, modify, and defend in an interview.
