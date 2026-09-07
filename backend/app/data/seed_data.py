"""Dados de exemplo para popular o banco em desenvolvimento e na demo.

Separado da lógica de inserção (`app/seed.py`) para ficar fácil de revisar e
estender só editando listas.
"""

# --------------------------------------------------------------------------- #
# Usuários                                                                     #
# --------------------------------------------------------------------------- #

USERS = [
    {"username": "ivan", "display_name": "Ivan", "is_guest": False},
    {"username": "gabriela", "display_name": "Gabriela", "is_guest": False},
    # Conta somente leitura para recrutadores navegarem sem login.
    {"username": "demo", "display_name": "Visitante", "is_guest": True},
]

# Atividade de exemplo criada no primeiro seed para o dashboard e a tela de
# revisão não aparecerem vazios numa demo. username -> notas de revisão.
DEMO_REVIEW_GRADES = {
    "ivan": [5, 4, 5, 3, 4, 5],
    "gabriela": [5, 5, 4, 5, 3, 4, 5, 4, 5],
}
# username -> slugs de cenários concluídos sem erro.
DEMO_SCENARIOS_DONE = {
    "ivan": ["anmeldung"],
    "gabriela": ["anmeldung", "konto-eroeffnen"],
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
    {"front_pt": "Eu preciso de um médico", "back_de": "Ich brauche einen Arzt", "phonetic_hint": "Írre bráu-rre áinen Ártst", "category": "saúde", "owner": "gabriela"},

    # Números
    {"front_pt": "Um / Dois / Três", "back_de": "eins / zwei / drei", "phonetic_hint": "áins / tsvái / drái", "category": "números", "owner": None},
    {"front_pt": "Quatro / Cinco / Seis", "back_de": "vier / fünf / sechs", "phonetic_hint": "fía / fünf / zeks", "category": "números", "owner": None},
    {"front_pt": "Sete / Oito / Nove / Dez", "back_de": "sieben / acht / neun / zehn", "phonetic_hint": "zíben / árrt / nóin / tsên", "category": "números", "owner": None},
    {"front_pt": "Vinte / Cinquenta / Cem", "back_de": "zwanzig / fünfzig / hundert", "phonetic_hint": "tsvántsirr / fünf-tsirr / húndert", "category": "números", "owner": None},

    # Tempo
    {"front_pt": "Que horas são?", "back_de": "Wie spät ist es?", "phonetic_hint": "Ví chpét ist es?", "category": "tempo", "owner": None},
    {"front_pt": "Hoje / Amanhã / Ontem", "back_de": "heute / morgen / gestern", "phonetic_hint": "hóite / mórguen / guéstern", "category": "tempo", "owner": None},
    {"front_pt": "agora / mais tarde / depois", "back_de": "jetzt / später / nachher", "phonetic_hint": "iétst / chpéta / nárr-hér", "category": "tempo", "owner": None},
    {"front_pt": "Segunda-feira / sexta-feira", "back_de": "Montag / Freitag", "phonetic_hint": "Móntak / Fráitak", "category": "tempo", "owner": None},
    {"front_pt": "o fim de semana", "back_de": "das Wochenende", "phonetic_hint": "das Vórren-ende", "category": "tempo", "owner": None},

    # Família e pessoas
    {"front_pt": "minha esposa / meu marido", "back_de": "meine Frau / mein Mann", "phonetic_hint": "máine Fráu / máin Man", "category": "família", "owner": None},
    {"front_pt": "meu filho / minha filha", "back_de": "mein Sohn / meine Tochter", "phonetic_hint": "máin Zón / máine Tórrter", "category": "família", "owner": None},
    {"front_pt": "os meus pais", "back_de": "meine Eltern", "phonetic_hint": "máine Éltern", "category": "família", "owner": None},
    {"front_pt": "um amigo / uma amiga", "back_de": "ein Freund / eine Freundin", "phonetic_hint": "áin Fróint / áine Fróindin", "category": "família", "owner": None},

    # Comida e bebida
    {"front_pt": "água sem gás", "back_de": "stilles Wasser", "phonetic_hint": "chtíles Váser", "category": "comida", "owner": None},
    {"front_pt": "um café, por favor", "back_de": "einen Kaffee, bitte", "phonetic_hint": "áinen Káfe, bíte", "category": "comida", "owner": None},
    {"front_pt": "pão / queijo / presunto", "back_de": "Brot / Käse / Schinken", "phonetic_hint": "Brót / Kéze / Chínken", "category": "comida", "owner": None},
    {"front_pt": "Eu sou vegetariano", "back_de": "Ich bin Vegetarier", "phonetic_hint": "írre bin vegue-tárier", "category": "comida", "owner": None},
    {"front_pt": "Isto é sem lactose?", "back_de": "Ist das laktosefrei?", "phonetic_hint": "ist das lak-tóze-frái?", "category": "comida", "owner": None},
    {"front_pt": "Está uma delícia", "back_de": "Es schmeckt sehr gut", "phonetic_hint": "es chméckt zea gút", "category": "comida", "owner": None},

    # No supermercado
    {"front_pt": "Onde encontro os ovos?", "back_de": "Wo finde ich die Eier?", "phonetic_hint": "Vô fínde írre di Áier?", "category": "compras", "owner": None},
    {"front_pt": "Vocês aceitam cartão?", "back_de": "Nehmen Sie Karte?", "phonetic_hint": "Némen zi Kárte?", "category": "compras", "owner": None},
    {"front_pt": "Uma sacola, por favor", "back_de": "Eine Tüte, bitte", "phonetic_hint": "áine Tüte, bíte", "category": "compras", "owner": None},
    {"front_pt": "É só isso, obrigado", "back_de": "Das ist alles, danke", "phonetic_hint": "das ist áles, dánke", "category": "compras", "owner": None},

    # Direções e transporte
    {"front_pt": "à esquerda / à direita / em frente", "back_de": "links / rechts / geradeaus", "phonetic_hint": "línks / rérrts / gue-ráde-áus", "category": "transporte", "owner": None},
    {"front_pt": "Onde fica o banheiro?", "back_de": "Wo ist die Toilette?", "phonetic_hint": "Vô ist di toa-léte?", "category": "transporte", "owner": None},
    {"front_pt": "Um bilhete para o centro", "back_de": "Eine Fahrkarte ins Zentrum", "phonetic_hint": "áine Fár-kárte ins Tséntrum", "category": "transporte", "owner": None},
    {"front_pt": "Este trem para em...?", "back_de": "Hält dieser Zug in...?", "phonetic_hint": "hélt díza Tsúk in...?", "category": "transporte", "owner": None},
    {"front_pt": "Eu me perdi", "back_de": "Ich habe mich verlaufen", "phonetic_hint": "írre hábe mírr fer-láufen", "category": "transporte", "owner": None},
    {"front_pt": "Quanto tempo demora?", "back_de": "Wie lange dauert es?", "phonetic_hint": "Ví lánge dáuert es?", "category": "transporte", "owner": None},

    # No restaurante
    {"front_pt": "Uma mesa para dois", "back_de": "Einen Tisch für zwei", "phonetic_hint": "áinen Tich fü tsvái", "category": "restaurante", "owner": None},
    {"front_pt": "O cardápio, por favor", "back_de": "Die Speisekarte, bitte", "phonetic_hint": "di Chpáize-kárte, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Eu gostaria de pedir", "back_de": "Ich möchte bestellen", "phonetic_hint": "írre mérrte be-chtélen", "category": "restaurante", "owner": None},
    {"front_pt": "Podemos pagar separado?", "back_de": "Können wir getrennt zahlen?", "phonetic_hint": "kénen vía gue-trént tsálen?", "category": "restaurante", "owner": None},
    {"front_pt": "Pode ficar com o troco", "back_de": "Stimmt so", "phonetic_hint": "chtimt zô", "category": "restaurante", "owner": None},

    # Saúde e emergência
    {"front_pt": "Estou me sentindo mal", "back_de": "Mir ist schlecht", "phonetic_hint": "Mía ist chlérrt", "category": "saúde", "owner": None},
    {"front_pt": "Dói aqui", "back_de": "Es tut hier weh", "phonetic_hint": "es tút hía vê", "category": "saúde", "owner": None},
    {"front_pt": "Preciso de uma farmácia", "back_de": "Ich brauche eine Apotheke", "phonetic_hint": "írre bráurre áine apo-téke", "category": "saúde", "owner": None},
    {"front_pt": "Chame uma ambulância!", "back_de": "Rufen Sie einen Krankenwagen!", "phonetic_hint": "Rúfen zi áinen Kránken-vágen!", "category": "saúde", "owner": None},
    {"front_pt": "Sou alérgico a...", "back_de": "Ich bin allergisch gegen...", "phonetic_hint": "írre bin a-lér-guich guéguen...", "category": "saúde", "owner": None},
    {"front_pt": "Tenho consulta às três", "back_de": "Ich habe einen Termin um drei", "phonetic_hint": "írre hábe áinen ter-mín um drái", "category": "saúde", "owner": None},

    # Conversa
    {"front_pt": "De onde você é?", "back_de": "Woher kommen Sie?", "phonetic_hint": "vo-hér kómen zi?", "category": "conversa", "owner": None},
    {"front_pt": "Eu sou do Brasil", "back_de": "Ich komme aus Brasilien", "phonetic_hint": "írre kóme áus bra-zílien", "category": "conversa", "owner": None},
    {"front_pt": "Estou aprendendo alemão", "back_de": "Ich lerne Deutsch", "phonetic_hint": "írre lérne dóitch", "category": "conversa", "owner": None},
    {"front_pt": "Pode falar mais devagar?", "back_de": "Können Sie langsamer sprechen?", "phonetic_hint": "kénen zi láng-zamer chpré-rren?", "category": "conversa", "owner": None},
    {"front_pt": "Como se diz ... em alemão?", "back_de": "Wie sagt man ... auf Deutsch?", "phonetic_hint": "ví zákt man ... áuf dóitch?", "category": "conversa", "owner": None},
    {"front_pt": "Bem, obrigado. E o senhor?", "back_de": "Danke, gut. Und Ihnen?", "phonetic_hint": "dánke, gút. unt ínen?", "category": "conversa", "owner": None},

    # Frases úteis
    {"front_pt": "Pode me ajudar?", "back_de": "Können Sie mir helfen?", "phonetic_hint": "kénen zi mía hélfen?", "category": "básico", "owner": None},
    {"front_pt": "Não tem problema", "back_de": "Macht nichts", "phonetic_hint": "márrt nírrts", "category": "básico", "owner": None},
    {"front_pt": "Eu quero / Eu queria", "back_de": "Ich will / Ich möchte", "phonetic_hint": "írre vil / írre mérrte", "category": "básico", "owner": None},
    {"front_pt": "Eu concordo / não concordo", "back_de": "Ich stimme zu / nicht zu", "phonetic_hint": "írre chtíme tsú / nírrt tsú", "category": "básico", "owner": None},

    # Moradia
    {"front_pt": "Procuro um apartamento", "back_de": "Ich suche eine Wohnung", "phonetic_hint": "írre zúrre áine Vônung", "category": "moradia", "owner": None},
    {"front_pt": "Qual é o valor do aluguel?", "back_de": "Wie hoch ist die Miete?", "phonetic_hint": "ví hôrr ist di Míte?", "category": "moradia", "owner": None},
    {"front_pt": "O aquecimento não funciona", "back_de": "Die Heizung funktioniert nicht", "phonetic_hint": "di Háitsung funk-tsio-nírt nírrt", "category": "moradia", "owner": None},
    {"front_pt": "Quando posso me mudar?", "back_de": "Wann kann ich einziehen?", "phonetic_hint": "van kan írre áin-tsíen?", "category": "moradia", "owner": None},

    # Trabalho
    {"front_pt": "Tenho uma reunião às dez", "back_de": "Ich habe ein Meeting um zehn", "phonetic_hint": "írre hábe áin míting um tsên", "category": "trabalho", "owner": None},
    {"front_pt": "Podemos remarcar?", "back_de": "Können wir verschieben?", "phonetic_hint": "kénen vía fer-chíben?", "category": "trabalho", "owner": None},
    {"front_pt": "Vou enviar por email", "back_de": "Ich schicke es per E-Mail", "phonetic_hint": "írre chíke es per í-mêil", "category": "trabalho", "owner": None},
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
    {
        "slug": "beim-arzt",
        "title": "Consulta com o médico",
        "description": (
            "Você vai ao médico com dor de garganta. Descreva os sintomas de forma "
            "clara e objetiva — é o que o médico espera."
        ),
        "category": "saúde",
        "steps": [
            {
                "speaker_de": "Guten Tag, was fehlt Ihnen?",
                "speaker_pt": "Bom dia, o que o senhor tem?",
                "options": [
                    {"text_de": "Ich habe seit gestern Halsschmerzen.", "correct": True,
                     "explanation": "'seit gestern' + o sintoma exato é o que o médico precisa para começar. Direto ao ponto."},
                    {"text_de": "Mir geht es nicht gut.", "correct": False,
                     "explanation": "Verdadeiro, mas vago; o médico teria que perguntar tudo de novo."},
                    {"text_de": "Ich brauche Medikamente.", "correct": False,
                     "explanation": "Quem decide isso é o médico; primeiro descreva o sintoma."},
                ],
            },
            {
                "speaker_de": "Haben Sie auch Fieber?",
                "speaker_pt": "O senhor também está com febre?",
                "options": [
                    {"text_de": "Ja, 38 Grad heute Morgen.", "correct": True,
                     "explanation": "Responder com o número mostra que você mediu — informação útil e objetiva."},
                    {"text_de": "Vielleicht.", "correct": False,
                     "explanation": "'Talvez' não ajuda o diagnóstico; se não sabe, diga que não mediu."},
                    {"text_de": "Ich hasse Fieber.", "correct": False,
                     "explanation": "Comentário pessoal fora de contexto."},
                ],
            },
            {
                "speaker_de": "Ich verschreibe Ihnen etwas. Sind Sie gegen Penicillin allergisch?",
                "speaker_pt": "Vou receitar um remédio. O senhor é alérgico a penicilina?",
                "options": [
                    {"text_de": "Nein, ich vertrage Penicillin.", "correct": True,
                     "explanation": "Confirmar a ausência de alergia com 'ich vertrage' é a formulação padrão."},
                    {"text_de": "Keine Ahnung.", "correct": False,
                     "explanation": "Alergia a antibiótico é sério; se não sabe, diga que nunca tomou — não deixe no ar."},
                    {"text_de": "Ja, aber das ist egal.", "correct": False,
                     "explanation": "Dizer que é alérgico e que 'tanto faz' pode causar uma reação grave. Nunca minimize isso."},
                ],
            },
        ],
    },
    {
        "slug": "im-supermarkt",
        "title": "No supermercado",
        "description": "Você procura alguns itens no supermercado e vai ao caixa.",
        "category": "compras",
        "steps": [
            {
                "speaker_de": "Kann ich Ihnen helfen?",
                "speaker_pt": "Posso ajudar?",
                "options": [
                    {"text_de": "Ja, wo finde ich Joghurt?", "correct": True,
                     "explanation": "'Wo finde ich...?' é a pergunta padrão para localizar um produto."},
                    {"text_de": "Ich suche etwas.", "correct": False,
                     "explanation": "Vago demais; diga o que procura."},
                    {"text_de": "Haben Sie Joghurt?", "correct": False,
                     "explanation": "O supermercado obviamente tem; a dúvida é onde, não se tem."},
                ],
            },
            {
                "speaker_de": "Der ist im Kühlregal, Gang 4. Sonst noch etwas?",
                "speaker_pt": "Fica na geladeira, corredor 4. Mais alguma coisa?",
                "options": [
                    {"text_de": "Nein danke, das war's.", "correct": True,
                     "explanation": "'das war's' encerra a interação de forma natural."},
                    {"text_de": "Ich weiß nicht.", "correct": False,
                     "explanation": "Indecisão trava a conversa; se acabou, diga que acabou."},
                    {"text_de": "Warum Gang 4?", "correct": False,
                     "explanation": "Questionar a localização não faz sentido; agradeça e vá."},
                ],
            },
            {
                "speaker_de": "Zusammen 12,40 Euro. Zahlen Sie mit Karte?",
                "speaker_pt": "Dá 12,40 no total. Vai pagar com cartão?",
                "options": [
                    {"text_de": "Ja, mit Karte, bitte.", "correct": True,
                     "explanation": "Resposta direta; muitos caixas menores preferem saber antes de finalizar."},
                    {"text_de": "Ich habe nur einen großen Schein.", "correct": False,
                     "explanation": "Não responde à pergunta; diga cartão ou dinheiro primeiro."},
                    {"text_de": "Ist das nicht zu teuer?", "correct": False,
                     "explanation": "Discutir o preço no caixa não leva a nada."},
                ],
            },
        ],
    },
    {
        "slug": "beim-baecker",
        "title": "Na padaria",
        "description": "De manhã cedo, você entra numa padaria para comprar pão e um café.",
        "category": "compras",
        "steps": [
            {
                "speaker_de": "Guten Morgen, was darf's sein?",
                "speaker_pt": "Bom dia, o que vai ser?",
                "options": [
                    {"text_de": "Zwei Brötchen und einen Kaffee zum Mitnehmen, bitte.", "correct": True,
                     "explanation": "Quantidade + item + 'zum Mitnehmen' (para viagem) numa frase só — exatamente o esperado."},
                    {"text_de": "Was haben Sie?", "correct": False,
                     "explanation": "Perguntar o cardápio inteiro numa fila de manhã é pouco prático; olhe a vitrine."},
                    {"text_de": "Ich will Brot.", "correct": False,
                     "explanation": "'Ich will' soa rude e 'Brot' sem quantidade obriga outra pergunta."},
                ],
            },
            {
                "speaker_de": "Möchten Sie die Brötchen aufgeschnitten?",
                "speaker_pt": "Quer os pãezinhos cortados?",
                "options": [
                    {"text_de": "Nein danke, so ist gut.", "correct": True,
                     "explanation": "'so ist gut' é a forma natural de recusar educadamente."},
                    {"text_de": "Was heißt aufgeschnitten?", "correct": False,
                     "explanation": "Trava a fila; nesse caso um simples 'ja' ou 'nein' resolve."},
                    {"text_de": "Egal.", "correct": False,
                     "explanation": "'Tanto faz' soa desinteressado; dê uma resposta clara."},
                ],
            },
            {
                "speaker_de": "Das macht 4,20 Euro.",
                "speaker_pt": "Dá 4,20 euros.",
                "options": [
                    {"text_de": "Hier, bitte. Stimmt so.", "correct": True,
                     "explanation": "Entregar o dinheiro com 'stimmt so' (pode ficar com o troco) é padrão em valores pequenos."},
                    {"text_de": "Ich zahle mit einer 50.", "correct": False,
                     "explanation": "Nota grande para compra pequena irrita; tenha trocado ou pague com cartão."},
                    {"text_de": "So teuer?", "correct": False,
                     "explanation": "Reclamar do preço na padaria não cai bem."},
                ],
            },
        ],
    },
    {
        "slug": "termin-am-telefon",
        "title": "Marcar consulta por telefone",
        "description": "Você liga para o consultório médico para agendar uma consulta.",
        "category": "telefone",
        "steps": [
            {
                "speaker_de": "Praxis Dr. Weber, guten Tag.",
                "speaker_pt": "Consultório Dr. Weber, bom dia.",
                "options": [
                    {"text_de": "Guten Tag, ich möchte einen Termin vereinbaren.", "correct": True,
                     "explanation": "'einen Termin vereinbaren' é a fórmula exata para marcar consulta."},
                    {"text_de": "Ich bin krank.", "correct": False,
                     "explanation": "Direto demais e não diz o que você quer da ligação."},
                    {"text_de": "Sind Sie der Arzt?", "correct": False,
                     "explanation": "Você ligou para a recepção; pergunta desnecessária."},
                ],
            },
            {
                "speaker_de": "Waren Sie schon einmal bei uns?",
                "speaker_pt": "O senhor já foi atendido aqui antes?",
                "options": [
                    {"text_de": "Nein, ich bin neu und gesetzlich versichert.", "correct": True,
                     "explanation": "Dizer que é novo + o tipo de plano (gesetzlich/privat) adianta o cadastro."},
                    {"text_de": "Ich glaube nicht.", "correct": False,
                     "explanation": "Ou você já foi ou não; a recepção precisa de certeza."},
                    {"text_de": "Ist das wichtig?", "correct": False,
                     "explanation": "É sim — muda o cadastro e os horários disponíveis."},
                ],
            },
            {
                "speaker_de": "Wir haben einen Termin am Donnerstag um 9 Uhr. Passt das?",
                "speaker_pt": "Temos um horário na quinta às 9h. Serve?",
                "options": [
                    {"text_de": "Ja, das passt. Vielen Dank.", "correct": True,
                     "explanation": "Confirmar com 'das passt' e agradecer fecha a ligação de forma limpa."},
                    {"text_de": "Vielleicht.", "correct": False,
                     "explanation": "A recepção precisa reservar ou liberar o horário; responda sim ou não."},
                    {"text_de": "Donnerstag ist schlecht, aber egal.", "correct": False,
                     "explanation": "Contradição: se não serve, diga e peça outro horário — aceitar 'de qualquer jeito' gera falta."},
                ],
            },
        ],
    },
]
