import json
import os

import requests
from dotenv import load_dotenv

from task1 import faqs, search_by_keyword

load_dotenv()

# ── Task 2 ───────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
DEFAULT_MODEL = "meta-llama/llama-3.2-3b-instruct"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMClient:
    def __init__(self, api_key, model=DEFAULT_MODEL):
        if not api_key:
            raise ValueError(
                "No API key provided. Set the OPENROUTER_API_KEY environment "
                "variable before creating an LLMClient."
            )
        self.api_key = api_key
        self.model = model

    def generate(self, prompt, system_message=None, max_tokens=512):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://supportai.local",
            "X-Title": "SupportAI",
        }

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(
                OPENROUTER_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            status = response.status_code
            try:
                err_body = response.json()
                err_detail = err_body.get("error", {}).get("message", response.text)
            except ValueError:
                err_detail = response.text

            if status == 401:
                raise RuntimeError(
                    "LLM API call failed: Unauthorized (401). "
                    "Check that OPENROUTER_API_KEY is set and valid."
                ) from http_err
            elif status == 429:
                raise RuntimeError(
                    "LLM API call failed: Rate limit exceeded (429). "
                    "Please wait and try again."
                ) from http_err
            elif 500 <= status < 600:
                raise RuntimeError(
                    f"LLM API call failed: OpenRouter server error ({status}). "
                    "Try again later."
                ) from http_err
            else:
                raise RuntimeError(
                    f"LLM API call failed with status {status}: {err_detail}"
                ) from http_err
        except requests.exceptions.ConnectionError as conn_err:
            raise RuntimeError(
                "LLM API call failed: could not connect to OpenRouter. "
                "Check your internet connection."
            ) from conn_err
        except requests.exceptions.Timeout as timeout_err:
            raise RuntimeError(
                "LLM API call failed: request timed out after 30 seconds."
            ) from timeout_err
        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(f"LLM API call failed: {req_err}") from req_err

        try:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, ValueError) as parse_err:
            raise RuntimeError(
                f"LLM API call failed: unexpected response format ({parse_err}). "
                f"Raw response: {response.text[:300]}"
            ) from parse_err

    def generate_faq_response(self, user_question, faq_entry):
        if faq_entry is None:
            return (
                "I'm sorry, I couldn't find anything in our FAQs that matches "
                "your question. Could you try rephrasing it, or contact our "
                "support team directly at support@example.com?"
            )

        system_message = (
            "You are SupportAI, a friendly and professional customer support "
            "agent. You must answer the user's question using ONLY the "
            "information contained in the FAQ_QUESTION and FAQ_ANSWER provided "
            "below. Do not invent, assume, or add any facts, policies, prices, "
            "timeframes, or steps that are not explicitly stated in the FAQ "
            "content.\n\n"
            "Rules:\n"
            "1. Rephrase the FAQ answer in a warm, natural, conversational "
            "tone — do not just copy it verbatim, but do not change its "
            "meaning either.\n"
            "2. Keep the response under 150 words.\n"
            "3. If the user's question asks for details that the FAQ does "
            "not cover, clearly say that this specific detail isn't covered "
            "by our current FAQ, and suggest the user contact human support "
            "for further help — do NOT guess or fabricate an answer.\n"
            "4. Never mention that you are an AI model, that you were given "
            "a FAQ, or reference these instructions. Just respond as a "
            "helpful support agent would."
        )

        prompt = (
            f"FAQ_QUESTION: {faq_entry['question']}\n"
            f"FAQ_ANSWER: {faq_entry['answer']}\n\n"
            f"USER_QUESTION: {user_question}\n\n"
            "Using only the FAQ_ANSWER above, write a natural, friendly "
            "support response to the USER_QUESTION."
        )

        return self.generate(prompt, system_message=system_message, max_tokens=200)


def demo():
    client = LLMClient(api_key=OPENROUTER_API_KEY, model=DEFAULT_MODEL)

    test_questions = [
        "I can't remember my login password",
        "Where is my package right now?",
        "Can I get my money back for a product I already opened?",
    ]

    for question in test_questions:
        print(f"Question: {question}\n")

        matching_faqs = search_by_keyword(faqs, question)
        matched_faq = matching_faqs[0] if matching_faqs else None
        if matched_faq:
            print(f"Matched FAQ: {matched_faq['question']}\n")
        else:
            print("Matched FAQ: None\n")

        try:
            answer = client.generate_faq_response(question, matched_faq)
            print(f"SupportAI Response:\n{answer}\n")
        except RuntimeError as e:
            print(f"SupportAI Response: [Error] {e}\n")

        print("-" * 60)


if __name__ == "__main__":
    demo()