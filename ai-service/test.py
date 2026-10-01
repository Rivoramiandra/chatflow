
from schemas import ConversationRequest, Message
from groq_service import generate_responses


def main():

    conversation = ConversationRequest(
        conversation=[
            Message(
                role="client",
                content=(
                    "Ouais, tu sais, J'ADORE ÇA 😜 "
                    "On se voit quand ? Bisou entre les jambes ;)"
                )
            ),
            Message(
                role="agent",
                content=(
                    "Tu peux me dire ce que tu me ferais "
                    "si j'étais à côté de toi en ce moment ?"
                )
            ),
            Message(
                role="client",
                content=(
                    "Ma chère Kerstin, j’ai écrit ça à 00 h 41"
                )
            ),
            Message(
                role="agent",
                content=(
                    "Les longs préliminaires, c’est la clé d’une "
                    "relation sexuelle agréable, pas vrai ? "
                    "Peut-être en portant un uniforme sexy, "
                    "tu aimes les uniformes ?"
                )
            ),
            Message(
                role="client",
                content=(
                    "Je peux faire un strip-tease pour toi en uniforme, "
                    "ça va te rendre fou."
                )
            ),
            Message(
                role="agent",
                content="Oui, j’en ai envie ;) Quand ???"
            ),
        ],
        language="French",
        tone="auto",
    )

    print("\nGenerating responses...\n")

    result = generate_responses(conversation)

    print("=" * 60)
    print(f"Language: {result.language}")
    print(f"Topic: {result.topic}")
    print(f"Client intent: {result.client_intent}")
    print(f"Tone: {result.tone}")
    print("=" * 60)

    for response in result.responses:

        print(
            f"\n[{response.id}] "
            f"{response.style.upper()}"
        )

        print(f"Characters: {len(response.text)}")
        print(response.text)

        print("-" * 60)


if __name__ == "__main__":
    main()