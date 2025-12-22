# Diverse test queries for accuracy validation
# These are sample queries that would be used to validate the RAG system's accuracy

TEST_QUERIES = [
    # General understanding questions
    {
        "question": "What is the main topic of this book?",
        "expected_elements": ["artificial intelligence", "machine learning", "AI", "ML"],
        "category": "general"
    },
    {
        "question": "Can you summarize the key concepts covered in this book?",
        "expected_elements": ["neural networks", "deep learning", "algorithms", "data"],
        "category": "general"
    },
    
    # Specific content questions
    {
        "question": "Who developed the theory of relativity?",
        "expected_elements": ["einstein", "albert einstein"],
        "category": "specific"
    },
    {
        "question": "What are the three types of machine learning?",
        "expected_elements": ["supervised", "unsupervised", "reinforcement"],
        "category": "specific"
    },
    {
        "question": "Explain the difference between supervised and unsupervised learning",
        "expected_elements": ["labeled", "unlabeled", "training data"],
        "category": "specific"
    },
    
    # Conceptual questions
    {
        "question": "Why is machine learning important in today's world?",
        "expected_elements": ["automation", "data analysis", "prediction", "efficiency"],
        "category": "conceptual"
    },
    {
        "question": "What are the ethical considerations in AI development?",
        "expected_elements": ["privacy", "fairness", "transparency", "bias"],
        "category": "conceptual"
    },
    
    # Application questions
    {
        "question": "How is machine learning used in healthcare?",
        "expected_elements": ["diagnosis", "treatment", "medical imaging", "patient data"],
        "category": "application"
    },
    {
        "question": "What are common applications of natural language processing?",
        "expected_elements": ["translation", "chatbots", "voice recognition", "text analysis"],
        "category": "application"
    },
    
    # Comparative questions
    {
        "question": "Compare neural networks with traditional programming",
        "expected_elements": ["learning from data", "explicit rules", "pattern recognition"],
        "category": "comparative"
    },
    
    # Definition questions
    {
        "question": "Define artificial intelligence",
        "expected_elements": ["computer systems", "human-like intelligence", "learning", "problem solving"],
        "category": "definition"
    },
    {
        "question": "What is deep learning?",
        "expected_elements": ["neural networks", "multiple layers", "pattern recognition"],
        "category": "definition"
    },
    
    # Process questions
    {
        "question": "How does a machine learning model learn?",
        "expected_elements": ["training data", "pattern recognition", "iteration", "optimization"],
        "category": "process"
    },
    
    # Example questions
    {
        "question": "Give examples of supervised learning problems",
        "expected_elements": ["classification", "regression", "image recognition", "spam detection"],
        "category": "example"
    },
    
    # Historical questions
    {
        "question": "When was the term 'artificial intelligence' first coined?",
        "expected_elements": ["1956", "dartmouth conference", "john mccarthy"],
        "category": "historical"
    },
    
    # Technical questions
    {
        "question": "What is overfitting in machine learning?",
        "expected_elements": ["too well on training", "poor on new data", "generalization"],
        "category": "technical"
    },
    {
        "question": "Explain the concept of neural networks",
        "expected_elements": ["artificial neurons", "layers", "weights", "activation functions"],
        "category": "technical"
    },
    
    # Future-oriented questions
    {
        "question": "What are the future trends in AI?",
        "expected_elements": ["generative models", "ethics", "automation", "edge computing"],
        "category": "future"
    },
    
    # Limitation questions
    {
        "question": "What are the limitations of current AI systems?",
        "expected_elements": ["common sense", "context understanding", "data dependency", "interpretability"],
        "category": "limitation"
    },
    
    # Methodology questions
    {
        "question": "How do you evaluate a machine learning model?",
        "expected_elements": ["accuracy", "precision", "recall", "f1 score", "validation"],
        "category": "methodology"
    }
]

# Selected text isolation tests
SELECTED_TEXT_TESTS = [
    {
        "selected_text": "The theory of relativity was developed by Albert Einstein in the early 20th century.",
        "question": "Who developed the theory of relativity?",
        "expected_answer_contains": ["einstein", "albert einstein"],
        "should_not_contain": ["darwin", "newton", "tesla"]
    },
    {
        "selected_text": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
        "question": "What is machine learning?",
        "expected_answer_contains": ["subset", "artificial intelligence", "algorithms", "learn from data"],
        "should_not_contain": ["biology", "chemistry", "physics"]
    }
]