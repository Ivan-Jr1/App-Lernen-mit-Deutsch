"""Dados de exemplo para popular o banco em desenvolvimento e na demo.

Separado da lógica de inserção (`app/seed.py`) para ficar fácil de revisar e
estender só editando listas.
"""

# --------------------------------------------------------------------------- #
# Usuários                                                                     #
# --------------------------------------------------------------------------- #

USERS = [
    {"username": "ivan", "display_name": "Ivan", "is_guest": False},
    {"username": "esposa", "display_name": "Esposa", "is_guest": False},
    # Conta somente leitura para recrutadores navegarem sem login.
    {"username": "demo", "display_name": "Visitante", "is_guest": True},
]

# Atividade de exemplo criada no primeiro seed para o dashboard e a tela de
# revisão não aparecerem vazios numa demo. username -> notas de revisão.
DEMO_REVIEW_GRADES = {
    "ivan": [5, 4, 5, 3, 4, 5],
    "esposa": [5, 5, 4, 5, 3, 4, 5, 4, 5],
}
# username -> slugs de cenários concluídos sem erro.
DEMO_SCENARIOS_DONE = {
    "ivan": ["anmeldung"],
    "esposa": ["anmeldung", "konto-eroeffnen"],
}

# --------------------------------------------------------------------------- #
# Flashcards                                                                   #
# `owner`: None = compartilhado; ou o username do dono para um cartão privado. #
# --------------------------------------------------------------------------- #

CARDS = [
    {"front_pt": "Bom dia", "back_de": "Guten Morgen", "phonetic_hint": "Gúten Mórgen", "category": "saudações", "owner": None},
    {"front_pt": "Boa tarde", "back_de": "Guten Tag", "phonetic_hint": "Gúten Ták", "category": "saudações", "owner": None},
    {"front_pt": "Boa noite (ao chegar)", "back_de": "Guten Abend", "phonetic_hint": "Gúten Ábent", "category": "saudações", "owner": None},
    {"front_pt": "Tchau", "back_de": "Tschüss", "phonetic_hint": "Tchüss", "category": "saudações", "owner": None},
    {"front_pt": "Obrigado", "back_de": "Danke", "phonetic_hint": "Dânke", "category": "básico", "owner": None},
    {"front_pt": "Por favor / De nada", "back_de": "Bitte", "phonetic_hint": "Bíte", "category": "básico", "owner": None},
    {"front_pt": "Sim / Não", "back_de": "Ja / Nein", "phonetic_hint": "Iá / Náin", "category": "básico", "owner": None},
    {"front_pt": "Desculpe / Com licença", "back_de": "Entschuldigung", "phonetic_hint": "Ent-chúldigung", "category": "básico", "owner": None},
    {"front_pt": "Você fala inglês?", "back_de": "Sprechen Sie Englisch?", "phonetic_hint": "Chpré-renn zi Ênglich?", "category": "básico", "owner": None},
    {"front_pt": "Eu não entendo", "back_de": "Ich verstehe nicht", "phonetic_hint": "Írre fer-chtêe nírt", "category": "básico", "owner": None},
    {"front_pt": "Quanto custa isso?", "back_de": "Was kostet das?", "phonetic_hint": "Vas kóstet das?", "category": "compras", "owner": None},
    {"front_pt": "A conta, por favor", "back_de": "Die Rechnung, bitte", "phonetic_hint": "Di Rérr-nung, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Uma cerveja, por favor", "back_de": "Ein Bier, bitte", "phonetic_hint": "Áin Bía, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Onde fica a estação de trem?", "back_de": "Wo ist der Bahnhof?", "phonetic_hint": "Vô ist dea Bán-hof?", "category": "direções", "owner": None},
    {"front_pt": "Eu gostaria de me registrar", "back_de": "Ich möchte mich anmelden", "phonetic_hint": "Írre mérr-te mírr án-melden", "category": "burocracia", "owner": None},
    {"front_pt": "Eu trabalho com tecnologia da informação", "back_de": "Ich arbeite in der IT", "phonetic_hint": "Írre ár-baite in dea I-Tê", "category": "trabalho", "owner": "ivan"},
    {"front_pt": "Eu preciso de um médico", "back_de": "Ich brauche einen Arzt", "phonetic_hint": "Írre bráu-rre áinen Ártst", "category": "saúde", "owner": "esposa"},
]

# --------------------------------------------------------------------------- #
# Cenários de burocracia                                                       #
# Cada passo tem 2–3 opções; exatamente uma com "correct": True.               #
# --------------------------------------------------------------------------- #

SCENARIOS = [
    {
        "slug": "anmeldung",
        "title": "Anmeldung no Bürgeramt",
        "description": (
            "Você chega ao Bürgeramt para registrar seu endereço. Tenha em mãos o "
            "formulário preenchido e a Wohnungsgeberbestätigung (confirmação do locador)."
        ),
        "category": "registro",
        "steps": [
            {
                "speaker_de": "Guten Tag. Was kann ich für Sie tun?",
                "speaker_pt": "Bom dia. O que posso fazer pelo senhor?",
                "options": [
                    {"text_de": "Ich möchte mich anmelden.", "correct": True,
                     "explanation": "'sich anmelden' é o verbo exato para registrar o endereço — é a frase que o funcionário espera ouvir."},
                    {"text_de": "Ich will ein Konto.", "correct": False,
                     "explanation": "Isso é para abrir conta em banco; não tem relação com o registro de endereço."},
                    {"text_de": "Ich bin neu hier.", "correct": False,
                     "explanation": "Gramaticalmente ok, mas vago; o funcionário ainda precisaria perguntar o que você quer fazer."},
                ],
            },
            {
                "speaker_de": "Haben Sie die Wohnungsgeberbestätigung dabei?",
                "speaker_pt": "O senhor trouxe a confirmação do locador?",
                "options": [
                    {"text_de": "Ja, hier bitte.", "correct": True,
                     "explanation": "'hier bitte' é a forma natural de entregar um documento em alemão."},
                    {"text_de": "Was ist das?", "correct": False,
                     "explanation": "Esse documento é obrigatório para o registro; sem ele o atendimento não continua."},
                    {"text_de": "Nein, ich habe es vergessen.", "correct": False,
                     "explanation": "Sem a confirmação do locador não dá para concluir o Anmeldung — você teria que voltar outro dia."},
                ],
            },
            {
                "speaker_de": "Alles in Ordnung. Möchten Sie eine Meldebescheinigung?",
                "speaker_pt": "Está tudo certo. O senhor quer um comprovante de registro?",
                "options": [
                    {"text_de": "Ja, gerne.", "correct": True,
                     "explanation": "A Meldebescheinigung é exigida para abrir conta, contrato de celular etc. 'Ja, gerne' é a resposta educada padrão."},
                    {"text_de": "Nein, danke.", "correct": False,
                     "explanation": "Não é errado, mas você vai precisar desse comprovante logo em seguida."},
                    {"text_de": "Ich weiß nicht.", "correct": False,
                     "explanation": "Hesitar aqui só atrasa; o funcionário quer uma resposta objetiva."},
                ],
            },
        ],
    },
    {
        "slug": "konto-eroeffnen",
        "title": "Abrir conta no banco",
        "description": (
            "Você vai ao banco abrir uma conta corrente (Girokonto). Leve o passaporte "
            "e a Meldebescheinigung."
        ),
        "category": "banco",
        "steps": [
            {
                "speaker_de": "Guten Tag, wie kann ich Ihnen helfen?",
                "speaker_pt": "Bom dia, como posso ajudar?",
                "options": [
                    {"text_de": "Ich möchte ein Girokonto eröffnen.", "correct": True,
                     "explanation": "'Girokonto' é a conta do dia a dia e 'eröffnen' é o verbo certo para abrir conta."},
                    {"text_de": "Ich möchte Geld.", "correct": False,
                     "explanation": "Soa abrupto e não diz o que você quer fazer."},
                    {"text_de": "Haben Sie Konten?", "correct": False,
                     "explanation": "Pergunta estranha — obviamente o banco tem contas. Diga diretamente o que precisa."},
                ],
            },
            {
                "speaker_de": "Haben Sie einen Ausweis und eine Meldebescheinigung dabei?",
                "speaker_pt": "O senhor trouxe um documento de identidade e o comprovante de registro?",
                "options": [
                    {"text_de": "Ja, meinen Reisepass und die Meldebescheinigung.", "correct": True,
                     "explanation": "Dizer quais documentos você tem agiliza o processo e mostra preparo."},
                    {"text_de": "Nur meinen Pass.", "correct": False,
                     "explanation": "Sem a Meldebescheinigung a maioria dos bancos não abre a conta."},
                    {"text_de": "Ich habe einen Führerschein.", "correct": False,
                     "explanation": "A carteira de motorista brasileira normalmente não é aceita como identidade no banco."},
                ],
            },
            {
                "speaker_de": "Möchten Sie auch eine Kreditkarte?",
                "speaker_pt": "O senhor também quer um cartão de crédito?",
                "options": [
                    {"text_de": "Nein, eine Girocard reicht mir erstmal.", "correct": True,
                     "explanation": "A Girocard (débito) cobre o essencial na Alemanha; recusar com 'reicht mir erstmal' é natural."},
                    {"text_de": "Ja, alles.", "correct": False,
                     "explanation": "Aceitar tudo sem perguntar taxas pode gerar uma anuidade desnecessária."},
                    {"text_de": "Was ist eine Kreditkarte?", "correct": False,
                     "explanation": "Fingir não conhecer o produto atrapalha a conversa."},
                ],
            },
        ],
    },
    {
        "slug": "wohnungsbesichtigung",
        "title": "Visita a um apartamento",
        "description": (
            "Você visita um apartamento e conversa com o locador. Alemães valorizam "
            "objetividade e comprovação de renda — cause boa impressão."
        ),
        "category": "moradia",
        "steps": [
            {
                "speaker_de": "Schön, dass Sie da sind. Haben Sie Fragen zur Wohnung?",
                "speaker_pt": "Que bom que veio. Tem perguntas sobre o apartamento?",
                "options": [
                    {"text_de": "Ja, sind die Nebenkosten im Preis enthalten?", "correct": True,
                     "explanation": "Os 'Nebenkosten' (água, aquecimento) são decisivos no orçamento — é a primeira pergunta que um alemão faria."},
                    {"text_de": "Ist die Wohnung schön?", "correct": False,
                     "explanation": "Pergunta subjetiva demais; você está no local, forme sua própria opinião."},
                    {"text_de": "Warum ziehen die Vormieter aus?", "correct": False,
                     "explanation": "Pode soar intrusivo num primeiro contato; deixe para depois se for relevante."},
                ],
            },
            {
                "speaker_de": "Wie sieht es mit Ihrem Einkommen aus?",
                "speaker_pt": "Como está a sua situação de renda?",
                "options": [
                    {"text_de": "Ich habe einen unbefristeten Arbeitsvertrag und kann eine Gehaltsabrechnung zeigen.", "correct": True,
                     "explanation": "Contrato por tempo indeterminado + holerite é exatamente o que o locador quer ouvir para reduzir o risco."},
                    {"text_de": "Das geht Sie nichts an.", "correct": False,
                     "explanation": "Recusar responder praticamente elimina suas chances; comprovação de renda é padrão na Alemanha."},
                    {"text_de": "Ich verdiene genug.", "correct": False,
                     "explanation": "Vago; o locador precisa de números e documentos, não de garantias verbais."},
                ],
            },
            {
                "speaker_de": "Wann könnten Sie einziehen?",
                "speaker_pt": "Quando o senhor poderia se mudar?",
                "options": [
                    {"text_de": "Zum Ersten des nächsten Monats.", "correct": True,
                     "explanation": "Mudanças na Alemanha quase sempre começam no dia 1º do mês; a resposta soa organizada."},
                    {"text_de": "Irgendwann.", "correct": False,
                     "explanation": "Falta de compromisso passa a impressão de candidato pouco confiável."},
                    {"text_de": "Sofort, heute noch.", "correct": False,
                     "explanation": "Pressa exagerada levanta suspeita; contrato e Kaution levam alguns dias."},
                ],
            },
        ],
    },
]
