"""Complete conversational SupportAI helpdesk agent for Task 4."""

from dataclasses import dataclass
import logging
import random

from task1 import faqs
from task2 import DEFAULT_MODEL, LLMClient, OPENROUTER_API_KEY
from task3 import hybrid_search


logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Represent one user or assistant message in the conversation."""

    role: str
    content: str
    faq_id: str = None
    confidence: float = None


class SupportAgent:
    """Orchestrate FAQ matching, grounded responses, and escalation."""

    def __init__(self, faqs, llm_client, confidence_threshold=0.15):
        """Initialise the agent with FAQs, an LLM client, and a confidence threshold."""
        self.faqs = faqs
        self.llm_client = llm_client
        self.confidence_threshold = confidence_threshold
        self.conversation_history = []
        self.is_escalated = False
        self.low_confidence_streak = 0

    def handle_message(self, user_message):
        """Answer a user message using the best confident FAQ match."""
        self.conversation_history.append(ConversationTurn("user", user_message))
        try:
            matching_faqs = hybrid_search(self.faqs, user_message, top_k=1)
        except Exception as error:
            logger.exception(
                "FAQ matching failed (%s): %s",
                type(error).__name__,
                error,
            )
            matching_faqs = []
        best_match = matching_faqs[0] if matching_faqs else None

        # hybrid_search returns (faq_entry, confidence); this is the value
        # compared with the configured threshold, before any LLM request.
        if best_match and best_match[1] >= self.confidence_threshold:
            faq_entry, confidence = best_match
            try:
                if self.llm_client is None:
                    raise RuntimeError(
                        "LLM client is not configured; set OPENROUTER_API_KEY."
                    )
                response = self.llm_client.generate_faq_response(
                    user_message,
                    faq_entry,
                )
            except Exception as error:
                logger.exception(
                    "LLM response failed for %s at confidence %.4f (%s): %s",
                    faq_entry["id"],
                    confidence,
                    type(error).__name__,
                    error,
                )
                response = faq_entry["answer"]
            self.low_confidence_streak = 0
            assistant_turn = ConversationTurn(
                "assistant",
                response,
                faq_id=faq_entry["id"],
                confidence=confidence,
            )
        else:
            logger.info(
                "No confident FAQ match for %r; best score=%s, threshold=%.4f",
                user_message,
                best_match[1] if best_match else None,
                self.confidence_threshold,
            )
            response = (
                "I don't have information about that in my knowledge base. "
                "Would you like me to connect you with a human support agent?"
            )
            self.low_confidence_streak += 1
            assistant_turn = ConversationTurn(
                "assistant",
                response,
                confidence=0.0,
            )

        self.conversation_history.append(assistant_turn)
        return response

    def escalate(self, reason="User requested human support"):
        """Escalate the conversation and return a mock support ticket confirmation."""
        self.is_escalated = True
        ticket_id = f"TICKET-{random.randint(10000, 99999)}"
        response = (
            "Your request has been escalated to our support team.\n"
            f"Ticket ID: {ticket_id}\n"
            "Estimated response time: within 4 business hours."
        )
        self.conversation_history.append(
            ConversationTurn("assistant", response, confidence=0.0)
        )
        return response

    def get_conversation_summary(self):
        """Return a readable summary of all messages and matching metadata."""
        if not self.conversation_history:
            return "No conversation history."

        lines = []
        for turn in self.conversation_history:
            label = "You" if turn.role == "user" else "SupportAI"
            metadata = []
            if turn.faq_id:
                metadata.append(f"faq: {turn.faq_id}")
            if turn.confidence is not None:
                metadata.append(f"confidence: {turn.confidence:.4f}")
            suffix = f" [{', '.join(metadata)}]" if metadata else ""
            lines.append(f"{label}{suffix}: {turn.content}")
        return "\n".join(lines)

    def reset(self):
        """Clear the conversation and return the agent to its initial state."""
        self.conversation_history.clear()
        self.is_escalated = False
        self.low_confidence_streak = 0


def _print_response(agent, response):
    """Print the latest response with its FAQ and confidence metadata."""
    latest_turn = agent.conversation_history[-1]
    details = []
    if latest_turn.confidence is not None:
        details.append(f"confidence: {latest_turn.confidence:.4f}")
    if latest_turn.faq_id:
        details.append(f"faq: {latest_turn.faq_id}")
    metadata = f" [{', '.join(details)}]" if details else ""
    print(f"\nSupportAI{metadata}:\n{response}")


def run_chat(agent):
    """Run the interactive helpdesk interface and its supported commands."""
    print("=" * 44)
    print("        SupportAI - Helpdesk Agent")
    print("=" * 44)
    print("Ask a question, or use: history, escalate, reset, quit")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThank you for using SupportAI. Goodbye!")
            break

        command = user_input.lower()
        if command == "quit":
            print("Thank you for using SupportAI. Goodbye!")
            break
        if command == "history":
            print(f"\n{agent.get_conversation_summary()}")
            continue
        if command == "escalate":
            print(f"\nSupportAI:\n{agent.escalate()}")
            continue
        if command == "reset":
            agent.reset()
            print("\nSupportAI: Conversation reset. How can I help you?")
            continue
        if not user_input:
            print("SupportAI: Please enter a question or command.")
            continue

        response = agent.handle_message(user_input)
        _print_response(agent, response)
        if agent.low_confidence_streak >= 3:
            print(
                "SupportAI: These questions may be outside my FAQ scope. "
                "You can type 'escalate' to contact human support."
            )


def demonstrate_scenarios(agent):
    """Demonstrate clear, paraphrased, unmatched, and escalated scenarios."""
    scenarios = [
        "How do I reset my password?",
        "I forgot my login credentials",
        "What are your office hours in Tokyo?",
    ]

    print("\nEnd-to-end demonstration")
    for question in scenarios:
        print(f"\nYou: {question}")
        response = agent.handle_message(question)
        _print_response(agent, response)

    print("\nYou: escalate")
    print(f"\nSupportAI:\n{agent.escalate()}")


def main():
    """Create the configured agent and start the interactive chat."""
    if not OPENROUTER_API_KEY:
        raise SystemExit(
            "Set OPENROUTER_API_KEY in .env before running the helpdesk agent."
        )

    client = LLMClient(api_key=OPENROUTER_API_KEY, model=DEFAULT_MODEL)
    agent = SupportAgent(faqs, client)
    demonstrate_scenarios(agent)
    run_chat(agent)


if __name__ == "__main__":
    main()
