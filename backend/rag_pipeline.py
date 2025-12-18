"""
RAG Pipeline Implementation
Handles document chunking, vector store creation, and retrieval
"""
import os
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama

from config import settings
from embeddings import EmbeddingManager


class RAGPipeline:
    """RAG pipeline for YouTube video Q&A"""
    
    def __init__(self):
        """Initialize RAG pipeline with embeddings and vector store"""
        self.embedding_manager = EmbeddingManager()
        self.vector_store = None
        self.qa_chain = None
        self.current_video_id = None
    
    def _get_llm(self):
        """Initialize LLM based on provider configuration"""
        provider = settings.LLM_PROVIDER.lower()
        
        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set")
            return OpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name=settings.LLM_MODEL,
                temperature=0.7
            )
        
        elif provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set")
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.7
            )
        
        elif provider == "ollama":
            return Ollama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=0.7
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create optimized prompt template for YouTube Q&A"""
        template = """You are a helpful assistant that answers questions based ONLY on the provided YouTube video transcript.

Context from video transcript:
{context}

Instructions:
- Answer the question using ONLY the information from the transcript above
- If the answer is not in the transcript, respond with: "This information is not available in the video."
- Be concise and clear
- If timestamps are available, mention them when relevant
- Do not make up information or use knowledge outside the transcript

Question: {question}

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def process_transcript(self, video_id: str, transcript_text: str):
        """
        Process transcript and create vector store
        
        Args:
            video_id: YouTube video ID
            transcript_text: Full transcript text
        """
        # Reset if video changed
        if self.current_video_id != video_id:
            self.vector_store = None
            self.qa_chain = None
            self.current_video_id = video_id
        
        # Split transcript into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )
        
        # Create documents
        documents = [Document(page_content=transcript_text, metadata={"video_id": video_id})]
        chunks = text_splitter.split_documents(documents)
        
        # Create vector store
        if settings.VECTOR_DB_TYPE.lower() == "faiss":
            self.vector_store = FAISS.from_documents(
                chunks,
                self.embedding_manager.embeddings
            )
        elif settings.VECTOR_DB_TYPE.lower() == "chroma":
            # Use in-memory Chroma for simplicity
            self.vector_store = Chroma.from_documents(
                chunks,
                self.embedding_manager.embeddings
            )
        else:
            raise ValueError(f"Unsupported vector DB type: {settings.VECTOR_DB_TYPE}")
        
        # Create QA chain
        prompt = self._create_prompt_template()
        llm = self._get_llm()
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": settings.TOP_K_RESULTS}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def answer_question(self, question: str) -> Dict[str, any]:
        """
        Answer a question using RAG
        
        Args:
            question: User's question
        
        Returns:
            Dictionary with answer and metadata
        """
        if self.qa_chain is None:
            raise ValueError("Transcript not processed. Call process_transcript first.")
        
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result.get("source_documents", [])
            ]
        }
    
    def reset(self):
        """Reset pipeline for new video"""
        self.vector_store = None
        self.qa_chain = None
        self.current_video_id = None

