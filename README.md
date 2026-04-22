# Εφαρμογές Τεχνητής Νοημοσύνης -  Κώδικας μαθήματος

Ο κώδικας του μαθήματος χωρίζεται σε τρεις φακέλους: inference με γλωσσικά μοντέλα, άντληση άρθρων από arXiv, και ένα πλήρες RAG pipeline.

```
.
├── LLM_inference/
│   ├── llm_concepts.ipynb
│   ├── ollama_inference.ipynb
│   ├── gemini_inference.ipynb
│   ├── chat_cli/
│   │   ├── chat.py
│   │   └── model_config.py
│   └── pubmed_API/
│       └── search.py
├── arxivx/
│   └── fetch_papers.ipynb
├── RAG_demo/
│   ├── rag_pipeline.ipynb
│   └── chroma_db/
└── requirements.txt
```


## LLM_inference

**`llm_concepts.ipynb`** — Το βασικό θεωρητικό notebook. Δείχνει πώς λειτουργεί η tokenization, πώς αλλάζει η συμπεριφορά του μοντέλου με διαφορετικές τιμές temperature, τι είναι το few-shot prompting, το hallucination, το chain-of-thought και το knowledge cutoff. Όλα τρέχουν τοπικά μέσω Ollama, χωρίς API key.

**`ollama_inference.ipynb`** — Πρακτικά παραδείγματα inference με τοπικό μοντέλο (`qwen2.5:3b`): Q&A, system prompt, multi-turn συνομιλία, summarization, streaming. Χρησιμοποιεί το OpenAI-compatible endpoint του Ollama οπότε ο κώδικας είναι σχεδόν ίδιος με αυτόν για οποιοδήποτε cloud API.

**`gemini_inference.ipynb`** — Ίδια δομή με το παραπάνω αλλά με το Gemini 2.5 Flash μέσω Google API. Χρήσιμο για σύγκριση τοπικού vs cloud μοντέλου. Χρειάζεται Google API key.

**`chat_cli/chat.py`** — Chatbot τερματικού που συνδέεται στο Ollama. Υποστηρίζει streaming και κρατάει ιστορικό συνομιλίας. Οι ρυθμίσεις (μοντέλο, temperature κ.λπ.) είναι στο `model_config.py`.

```bash
python LLM_inference/chat_cli/chat.py --temperature 0.7
```

**`pubmed_API/search.py`** — Script που κάνει αναζήτηση στο PubMed (NCBI E-utilities API) και επιστρέφει τίτλους και abstracts για μια θεματική.


## arxivx

**`fetch_papers.ipynb`** — Κατεβάζει άρθρα από το arXiv με βάση ένα query (π.χ. `abs:"spiking neural network" AND cat:cs.CL`). Για κάθε άρθρο κατεβάζει το PDF, εξάγει το κείμενο με PyMuPDF και αποθηκεύει `.txt` + `.json` με τα metadata. Στο τέλος φτιάχνει ένα `catalog.json` που το διαβάζει το RAG notebook.



## RAG_demo

**`rag_pipeline.ipynb`** — Υλοποίηση ενός RAG pipeline από την αρχή. Φορτώνει τα άρθρα από το `arxivx/`, τα κόβει σε chunks με το `RecursiveCharacterTextSplitter`, δημιουργεί embeddings με `sentence-transformers` (`all-MiniLM-L6-v2`) και τα αποθηκεύει σε [ChromaDB](https://docs.trychroma.com/). Για κάθε ερώτηση του χρήστη ανακτά τα πιο σχετικά chunks και τα περνάει ως context στο `llama3.2:3b` μέσω Ollama.

Περιλαμβάνει επίσης οπτικοποίηση των embeddings σε 2D με t-SNE, και σύγκριση RAG vs no-RAG στην ίδια ερώτηση.



## Εγκατάσταση

Συνιστάται χρήση virtual environment ώστε οι βιβλιοθήκες του project να μην αναμειχθούν με το υπόλοιπο σύστημα:

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

Για να ανοίξετε τα notebooks:

```bash
jupyter notebook
```

### Ollama (για τοπικά μοντέλα)

Τα `llm_concepts.ipynb`, `ollama_inference.ipynb` και `rag_pipeline.ipynb` χρειάζονται [Ollama](https://ollama.com) να τρέχει στο παρασκήνιο:

```bash
ollama serve

# σε νέο terminal
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
```


## Απορίες

Για απορίες μπορείτε να στείλετε e-mail στο grammenos@ionio.gr 

## Βιβλιοθήκες

- [ChromaDB](https://docs.trychroma.com/) — vector database για τα embeddings του RAG
- [LangChain Text Splitters](https://python.langchain.com/docs/concepts/text_splitters/) — διαχωρισμός κειμένου σε chunks
- [sentence-transformers](https://sbert.net/) — δημιουργία embeddings τοπικά
