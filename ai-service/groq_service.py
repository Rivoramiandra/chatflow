
import json

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT, build_conversation_prompt
from schemas import (
    ConversationRequest,
    GenerateResponse,
)


client = Groq(api_key=GROQ_API_KEY)


def validate_conversation(
    request: ConversationRequest,
) -> None:

    conversation = request.conversation

    # Minimum 2 messages
    if len(conversation) < 2:
        raise ValueError(
            "La conversation doit contenir au moins 2 messages."
        )

    # Maximum 30 messages
    if len(conversation) > 30:
        raise ValueError(
            "La conversation ne peut pas contenir plus de 30 messages."
        )

    # Maximum 30 000 characters
    total_length = sum(
        len(message.content)
        for message in conversation
    )

    if total_length > 30000:
        raise ValueError(
            "La conversation est trop longue."
        )

    # At least one client message
    if not any(
        message.role == "client"
        for message in conversation
    ):
        raise ValueError(
            "La conversation doit contenir au moins un message client."
        )


def generate_responses(
    request: ConversationRequest,
) -> GenerateResponse:

    # 1. Validate conversation
    validate_conversation(request)

    # 2. Prepare conversation data
    conversation_data = [
        message.model_dump()
        for message in request.conversation
    ]

    # 3. Build prompt
    user_prompt = build_conversation_prompt(
        conversation=conversation_data,
        language=request.language,
        tone=request.tone,
    )

    # 4. Call Groq API
    try:

        response = client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            temperature=0.7,

            max_completion_tokens=4096,

            response_format={
                "type": "json_object"
            },
        )

    except Exception as error:

        raise RuntimeError(
            f"Erreur lors de l'appel à Groq : {error}"
        ) from error

    # 5. Retrieve generated content
    choice = response.choices[0]

    content = choice.message.content

    if not content:

        raise RuntimeError(
            "Groq n'a retourné aucun contenu. "
            f"Finish reason : {choice.finish_reason}"
        )

    # 6. Parse JSON
    try:

        data = json.loads(content)

    except json.JSONDecodeError as error:

        print("\n========== GROQ RAW OUTPUT ==========")
        print(content)
        print("=====================================\n")

        raise RuntimeError(
            "Groq a retourné un JSON invalide."
        ) from error

    # 7. Validate with Pydantic
    try:

        result = GenerateResponse.model_validate(data)

    except Exception as error:

        print("\n========== INVALID MODEL OUTPUT ==========")
        print(json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ))
        print("==========================================\n")

        raise RuntimeError(
            f"Structure JSON incorrecte : {error}"
        ) from error

    # 8. Verify exactly four suggestions
    if len(result.responses) != 4:

        raise RuntimeError(
            f"Le modèle a généré {len(result.responses)} réponses "
            "au lieu de 4."
        )

    # 9. Verify response IDs
    expected_ids = [1, 2, 3, 4]

    actual_ids = [
        item.id for item in result.responses
    ]

    if actual_ids != expected_ids:

        raise RuntimeError(
            f"Identifiants incorrects : {actual_ids}"
        )

    # 10. Verify non-empty suggestions
    for item in result.responses:

        if not item.text.strip():

            raise RuntimeError(
                f"La réponse numéro {item.id} est vide."
            )

    return result