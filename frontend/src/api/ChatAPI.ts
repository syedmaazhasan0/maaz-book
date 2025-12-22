// Chat API wrapper for Physical AI Chatbot
interface QueryRequest {
  question: string;
  book_id: string;
  selected_text?: string | null;
}

interface QueryResponse {
  answer: string;
  sources: string[];
  mode_used: string;
}

// Legacy response format for compatibility
interface LegacyQueryResponse {
  response: string;
  sources: string[];
  sessionId: string;
  timestamp: string;
}

class ChatAPI {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async sendMessage(
    question: string,
    selectedText?: string
  ): Promise<LegacyQueryResponse> {
    const payload: QueryRequest = {
      question: question,
      book_id: "physical-ai-book",
      selected_text: selectedText || null,
    };

    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    const data: QueryResponse = await response.json();

    // Convert to legacy format for compatibility with existing frontend
    return {
      response: data.answer,
      sources: data.sources,
      sessionId: `session-${Date.now()}`,
      timestamp: new Date().toISOString(),
    };
  }
}

export default ChatAPI;
export type { QueryRequest, QueryResponse };
