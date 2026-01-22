"""
RAG Pipeline for PDF processing and retrieval using OpenAI embeddings + LLM answering
"""

import PyPDF2
import numpy as np
from typing import List, Tuple
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class RAGPipeline:
    def __init__(self):
        self.documents = []
        self.embeddings = None

    def extract_text_from_pdf(self, pdf_file) -> str:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text

    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            if chunk.strip():
                chunks.append(chunk)
            start = end - overlap
            if start < 0:
                start = 0
        return chunks

    def add_pdf(self, pdf_file):
        text = self.extract_text_from_pdf(pdf_file)
        if not text.strip():
            raise ValueError("PDF contains no text")

        chunks = self.chunk_text(text)

        for c in chunks:
            self.documents.append(c)

        self._build_embeddings()

    def _build_embeddings(self):
        if not self.documents:
            return

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=self.documents
        )

        self.embeddings = np.array([x.embedding for x in response.data], dtype=np.float32)

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        if not self.documents or self.embeddings is None:
            return []

        q = client.embeddings.create(
            model="text-embedding-3-small",
            input=[query]
        ).data[0].embedding

        q = np.array(q, dtype=np.float32)

        from sklearn.metrics.pairwise import cosine_similarity
        sims = cosine_similarity([q], self.embeddings)[0]
        top = np.argsort(sims)[::-1][:k]

        return [self.documents[i] for i in top]

    def ask(self, query: str) -> str:
        if not self.documents:
            return "No documents uploaded yet."

        ctx = "\n\n".join(self.retrieve(query))

        prompt = f"""
Answer ONLY using the context below.

Context:
{ctx}

Question:
{query}

If not in context, say: The document does not contain this information.
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You answer only from given context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return res.choices[0].message.content.strip()

    def get_document_count(self):
        return len(self.documents)
