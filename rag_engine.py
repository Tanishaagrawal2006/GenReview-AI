import math
import re
from collections import Counter
from database import get_db_connection

def tokenize(text):
    text = text.lower()
    return re.findall(r'\b\w+\b', text)

def compute_tf(tokens):
    tf_dict = Counter(tokens)
    total = len(tokens)
    return {k: v / total for k, v in tf_dict.items()} if total > 0 else {}

def compute_idf(documents):
    idf_dict = {}
    total_docs = len(documents)
    all_words = set(word for doc in documents for word in doc)
    
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc)
        idf_dict[word] = math.log((total_docs + 1) / (doc_count + 1)) + 1
    return idf_dict

def compute_tfidf(tf, idf):
    return {k: v * idf.get(k, 0.0) for k, v in tf.items()}

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return numerator / denominator

def ingest_business_context(business_id):
   
    return True

def retrieve_context(business_id, query_text, top_k=4):
    
    try:
        conn = get_db_connection()
        documents = []
        sources = []
        
     
        feedbacks = conn.execute(
            "SELECT id, overall_rating, complaint_text, selected_draft_text, improvement_tags "
            "FROM feedback_records WHERE business_id = ? AND status = 'Resolved' "
            "AND (complaint_text IS NOT NULL OR selected_draft_text IS NOT NULL)", 
            (business_id,)
        ).fetchall()
        
        for f in feedbacks:
            text_parts = []
            if f['selected_draft_text']:
                text_parts.append(f"Approved Draft: {f['selected_draft_text']}")
            if f['complaint_text']:
                text_parts.append(f"Customer Complaint: {f['complaint_text']}")
                
            content = " | ".join(text_parts)
            documents.append(content)
            sources.append("FEEDBACK")
            
       
        knowledge_rows = conn.execute(
            "SELECT source_type, content FROM business_knowledge WHERE business_id = ?",
            (business_id,)
        ).fetchall()
        
        for k in knowledge_rows:
            documents.append(k['content'])
            sources.append(k['source_type'].upper())
            
        conn.close()
        
        if not documents:
            return ""
            
      
        tokenized_docs = [tokenize(doc) for doc in documents]
        idf = compute_idf(tokenized_docs)
        
        doc_vectors = []
        for doc_tokens in tokenized_docs:
            tf = compute_tf(doc_tokens)
            tfidf = compute_tfidf(tf, idf)
            doc_vectors.append(tfidf)
            
  
        query_tokens = tokenize(query_text)
        query_tf = compute_tf(query_tokens)
        query_vector = compute_tfidf(query_tf, idf)
        

        scores = []
        for i, doc_vector in enumerate(doc_vectors):
            score = cosine_similarity(query_vector, doc_vector)
            scores.append((score, i))
            
    
        scores.sort(reverse=True, key=lambda x: x[0])
        
   
        top_indices = [x[1] for x in scores[:top_k] if x[0] > 0.01] 
        
        if not top_indices:
            top_indices = [x[1] for x in scores[:top_k]]
            
        context_chunks = []
        for idx in top_indices:
            context_chunks.append(f"[{sources[idx]}] {documents[idx]}")
            
        return "\n".join(context_chunks)
    except Exception as e:
        print(f"Pure Python RAG Retrieval Error for Biz {business_id}: {str(e)}")
        return ""
