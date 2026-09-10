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
# `language`: ausente = "de" (o deck alemão original); "en" para o deck inglês. #
# --------------------------------------------------------------------------- #

CARDS = [
    {"front_pt": "Bom dia", "back_target": "Guten Morgen", "phonetic_hint": "Gúten Mórgen", "category": "saudações", "owner": None},
    {"front_pt": "Boa tarde", "back_target": "Guten Tag", "phonetic_hint": "Gúten Ták", "category": "saudações", "owner": None},
    {"front_pt": "Boa noite (ao chegar)", "back_target": "Guten Abend", "phonetic_hint": "Gúten Ábent", "category": "saudações", "owner": None},
    {"front_pt": "Tchau", "back_target": "Tschüss", "phonetic_hint": "Tchüss", "category": "saudações", "owner": None},
    {"front_pt": "Obrigado", "back_target": "Danke", "phonetic_hint": "Dânke", "category": "básico", "owner": None},
    {"front_pt": "Por favor / De nada", "back_target": "Bitte", "phonetic_hint": "Bíte", "category": "básico", "owner": None},
    {"front_pt": "Sim / Não", "back_target": "Ja / Nein", "phonetic_hint": "Iá / Náin", "category": "básico", "owner": None},
    {"front_pt": "Desculpe / Com licença", "back_target": "Entschuldigung", "phonetic_hint": "Ent-chúldigung", "category": "básico", "owner": None},
    {"front_pt": "Você fala inglês?", "back_target": "Sprechen Sie Englisch?", "phonetic_hint": "Chpré-renn zi Ênglich?", "category": "básico", "owner": None},
    {"front_pt": "Eu não entendo", "back_target": "Ich verstehe nicht", "phonetic_hint": "Írre fer-chtêe nírt", "category": "básico", "owner": None},
    {"front_pt": "Quanto custa isso?", "back_target": "Was kostet das?", "phonetic_hint": "Vas kóstet das?", "category": "compras", "owner": None},
    {"front_pt": "A conta, por favor", "back_target": "Die Rechnung, bitte", "phonetic_hint": "Di Rérr-nung, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Uma cerveja, por favor", "back_target": "Ein Bier, bitte", "phonetic_hint": "Áin Bía, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Onde fica a estação de trem?", "back_target": "Wo ist der Bahnhof?", "phonetic_hint": "Vô ist dea Bán-hof?", "category": "direções", "owner": None},
    {"front_pt": "Eu gostaria de me registrar", "back_target": "Ich möchte mich anmelden", "phonetic_hint": "Írre mérr-te mírr án-melden", "category": "burocracia", "owner": None},
    {"front_pt": "Eu trabalho com tecnologia da informação", "back_target": "Ich arbeite in der IT", "phonetic_hint": "Írre ár-baite in dea I-Tê", "category": "trabalho", "owner": "ivan"},
    {"front_pt": "Eu preciso de um médico", "back_target": "Ich brauche einen Arzt", "phonetic_hint": "Írre bráu-rre áinen Ártst", "category": "saúde", "owner": "gabriela"},

    # Números
    {"front_pt": "Um / Dois / Três", "back_target": "eins / zwei / drei", "phonetic_hint": "áins / tsvái / drái", "category": "números", "owner": None},
    {"front_pt": "Quatro / Cinco / Seis", "back_target": "vier / fünf / sechs", "phonetic_hint": "fía / fünf / zeks", "category": "números", "owner": None},
    {"front_pt": "Sete / Oito / Nove / Dez", "back_target": "sieben / acht / neun / zehn", "phonetic_hint": "zíben / árrt / nóin / tsên", "category": "números", "owner": None},
    {"front_pt": "Vinte / Cinquenta / Cem", "back_target": "zwanzig / fünfzig / hundert", "phonetic_hint": "tsvántsirr / fünf-tsirr / húndert", "category": "números", "owner": None},

    # Tempo
    {"front_pt": "Que horas são?", "back_target": "Wie spät ist es?", "phonetic_hint": "Ví chpét ist es?", "category": "tempo", "owner": None},
    {"front_pt": "Hoje / Amanhã / Ontem", "back_target": "heute / morgen / gestern", "phonetic_hint": "hóite / mórguen / guéstern", "category": "tempo", "owner": None},
    {"front_pt": "agora / mais tarde / depois", "back_target": "jetzt / später / nachher", "phonetic_hint": "iétst / chpéta / nárr-hér", "category": "tempo", "owner": None},
    {"front_pt": "Segunda-feira / sexta-feira", "back_target": "Montag / Freitag", "phonetic_hint": "Móntak / Fráitak", "category": "tempo", "owner": None},
    {"front_pt": "o fim de semana", "back_target": "das Wochenende", "phonetic_hint": "das Vórren-ende", "category": "tempo", "owner": None},

    # Família e pessoas
    {"front_pt": "minha esposa / meu marido", "back_target": "meine Frau / mein Mann", "phonetic_hint": "máine Fráu / máin Man", "category": "família", "owner": None},
    {"front_pt": "meu filho / minha filha", "back_target": "mein Sohn / meine Tochter", "phonetic_hint": "máin Zón / máine Tórrter", "category": "família", "owner": None},
    {"front_pt": "os meus pais", "back_target": "meine Eltern", "phonetic_hint": "máine Éltern", "category": "família", "owner": None},
    {"front_pt": "um amigo / uma amiga", "back_target": "ein Freund / eine Freundin", "phonetic_hint": "áin Fróint / áine Fróindin", "category": "família", "owner": None},

    # Comida e bebida
    {"front_pt": "água sem gás", "back_target": "stilles Wasser", "phonetic_hint": "chtíles Váser", "category": "comida", "owner": None},
    {"front_pt": "um café, por favor", "back_target": "einen Kaffee, bitte", "phonetic_hint": "áinen Káfe, bíte", "category": "comida", "owner": None},
    {"front_pt": "pão / queijo / presunto", "back_target": "Brot / Käse / Schinken", "phonetic_hint": "Brót / Kéze / Chínken", "category": "comida", "owner": None},
    {"front_pt": "Eu sou vegetariano", "back_target": "Ich bin Vegetarier", "phonetic_hint": "írre bin vegue-tárier", "category": "comida", "owner": None},
    {"front_pt": "Isto é sem lactose?", "back_target": "Ist das laktosefrei?", "phonetic_hint": "ist das lak-tóze-frái?", "category": "comida", "owner": None},
    {"front_pt": "Está uma delícia", "back_target": "Es schmeckt sehr gut", "phonetic_hint": "es chméckt zea gút", "category": "comida", "owner": None},

    # No supermercado
    {"front_pt": "Onde encontro os ovos?", "back_target": "Wo finde ich die Eier?", "phonetic_hint": "Vô fínde írre di Áier?", "category": "compras", "owner": None},
    {"front_pt": "Vocês aceitam cartão?", "back_target": "Nehmen Sie Karte?", "phonetic_hint": "Némen zi Kárte?", "category": "compras", "owner": None},
    {"front_pt": "Uma sacola, por favor", "back_target": "Eine Tüte, bitte", "phonetic_hint": "áine Tüte, bíte", "category": "compras", "owner": None},
    {"front_pt": "É só isso, obrigado", "back_target": "Das ist alles, danke", "phonetic_hint": "das ist áles, dánke", "category": "compras", "owner": None},

    # Direções e transporte
    {"front_pt": "à esquerda / à direita / em frente", "back_target": "links / rechts / geradeaus", "phonetic_hint": "línks / rérrts / gue-ráde-áus", "category": "transporte", "owner": None},
    {"front_pt": "Onde fica o banheiro?", "back_target": "Wo ist die Toilette?", "phonetic_hint": "Vô ist di toa-léte?", "category": "transporte", "owner": None},
    {"front_pt": "Um bilhete para o centro", "back_target": "Eine Fahrkarte ins Zentrum", "phonetic_hint": "áine Fár-kárte ins Tséntrum", "category": "transporte", "owner": None},
    {"front_pt": "Este trem para em...?", "back_target": "Hält dieser Zug in...?", "phonetic_hint": "hélt díza Tsúk in...?", "category": "transporte", "owner": None},
    {"front_pt": "Eu me perdi", "back_target": "Ich habe mich verlaufen", "phonetic_hint": "írre hábe mírr fer-láufen", "category": "transporte", "owner": None},
    {"front_pt": "Quanto tempo demora?", "back_target": "Wie lange dauert es?", "phonetic_hint": "Ví lánge dáuert es?", "category": "transporte", "owner": None},

    # No restaurante
    {"front_pt": "Uma mesa para dois", "back_target": "Einen Tisch für zwei", "phonetic_hint": "áinen Tich fü tsvái", "category": "restaurante", "owner": None},
    {"front_pt": "O cardápio, por favor", "back_target": "Die Speisekarte, bitte", "phonetic_hint": "di Chpáize-kárte, bíte", "category": "restaurante", "owner": None},
    {"front_pt": "Eu gostaria de pedir", "back_target": "Ich möchte bestellen", "phonetic_hint": "írre mérrte be-chtélen", "category": "restaurante", "owner": None},
    {"front_pt": "Podemos pagar separado?", "back_target": "Können wir getrennt zahlen?", "phonetic_hint": "kénen vía gue-trént tsálen?", "category": "restaurante", "owner": None},
    {"front_pt": "Pode ficar com o troco", "back_target": "Stimmt so", "phonetic_hint": "chtimt zô", "category": "restaurante", "owner": None},

    # Saúde e emergência
    {"front_pt": "Estou me sentindo mal", "back_target": "Mir ist schlecht", "phonetic_hint": "Mía ist chlérrt", "category": "saúde", "owner": None},
    {"front_pt": "Dói aqui", "back_target": "Es tut hier weh", "phonetic_hint": "es tút hía vê", "category": "saúde", "owner": None},
    {"front_pt": "Preciso de uma farmácia", "back_target": "Ich brauche eine Apotheke", "phonetic_hint": "írre bráurre áine apo-téke", "category": "saúde", "owner": None},
    {"front_pt": "Chame uma ambulância!", "back_target": "Rufen Sie einen Krankenwagen!", "phonetic_hint": "Rúfen zi áinen Kránken-vágen!", "category": "saúde", "owner": None},
    {"front_pt": "Sou alérgico a...", "back_target": "Ich bin allergisch gegen...", "phonetic_hint": "írre bin a-lér-guich guéguen...", "category": "saúde", "owner": None},
    {"front_pt": "Tenho consulta às três", "back_target": "Ich habe einen Termin um drei", "phonetic_hint": "írre hábe áinen ter-mín um drái", "category": "saúde", "owner": None},

    # Conversa
    {"front_pt": "De onde você é?", "back_target": "Woher kommen Sie?", "phonetic_hint": "vo-hér kómen zi?", "category": "conversa", "owner": None},
    {"front_pt": "Eu sou do Brasil", "back_target": "Ich komme aus Brasilien", "phonetic_hint": "írre kóme áus bra-zílien", "category": "conversa", "owner": None},
    {"front_pt": "Estou aprendendo alemão", "back_target": "Ich lerne Deutsch", "phonetic_hint": "írre lérne dóitch", "category": "conversa", "owner": None},
    {"front_pt": "Pode falar mais devagar?", "back_target": "Können Sie langsamer sprechen?", "phonetic_hint": "kénen zi láng-zamer chpré-rren?", "category": "conversa", "owner": None},
    {"front_pt": "Como se diz ... em alemão?", "back_target": "Wie sagt man ... auf Deutsch?", "phonetic_hint": "ví zákt man ... áuf dóitch?", "category": "conversa", "owner": None},
    {"front_pt": "Bem, obrigado. E o senhor?", "back_target": "Danke, gut. Und Ihnen?", "phonetic_hint": "dánke, gút. unt ínen?", "category": "conversa", "owner": None},

    # Frases úteis
    {"front_pt": "Pode me ajudar?", "back_target": "Können Sie mir helfen?", "phonetic_hint": "kénen zi mía hélfen?", "category": "básico", "owner": None},
    {"front_pt": "Não tem problema", "back_target": "Macht nichts", "phonetic_hint": "márrt nírrts", "category": "básico", "owner": None},
    {"front_pt": "Eu quero / Eu queria", "back_target": "Ich will / Ich möchte", "phonetic_hint": "írre vil / írre mérrte", "category": "básico", "owner": None},
    {"front_pt": "Eu concordo / não concordo", "back_target": "Ich stimme zu / nicht zu", "phonetic_hint": "írre chtíme tsú / nírrt tsú", "category": "básico", "owner": None},

    # Moradia
    {"front_pt": "Procuro um apartamento", "back_target": "Ich suche eine Wohnung", "phonetic_hint": "írre zúrre áine Vônung", "category": "moradia", "owner": None},
    {"front_pt": "Qual é o valor do aluguel?", "back_target": "Wie hoch ist die Miete?", "phonetic_hint": "ví hôrr ist di Míte?", "category": "moradia", "owner": None},
    {"front_pt": "O aquecimento não funciona", "back_target": "Die Heizung funktioniert nicht", "phonetic_hint": "di Háitsung funk-tsio-nírt nírrt", "category": "moradia", "owner": None},
    {"front_pt": "Quando posso me mudar?", "back_target": "Wann kann ich einziehen?", "phonetic_hint": "van kan írre áin-tsíen?", "category": "moradia", "owner": None},

    # Trabalho
    {"front_pt": "Tenho uma reunião às dez", "back_target": "Ich habe ein Meeting um zehn", "phonetic_hint": "írre hábe áin míting um tsên", "category": "trabalho", "owner": None},
    {"front_pt": "Podemos remarcar?", "back_target": "Können wir verschieben?", "phonetic_hint": "kénen vía fer-chíben?", "category": "trabalho", "owner": None},
    {"front_pt": "Vou enviar por email", "back_target": "Ich schicke es per E-Mail", "phonetic_hint": "írre chíke es per í-mêil", "category": "trabalho", "owner": None},

    # ----------------------------------------------------------------------- #
    # Deck de inglês                                                          #
    # ----------------------------------------------------------------------- #

    # Saudações e básico
    {"front_pt": "Bom dia", "back_target": "Good morning", "phonetic_hint": "Gud mórning", "category": "saudações", "owner": None, "language": "en"},
    {"front_pt": "Boa tarde", "back_target": "Good afternoon", "phonetic_hint": "Gud after-nún", "category": "saudações", "owner": None, "language": "en"},
    {"front_pt": "Boa noite (ao chegar)", "back_target": "Good evening", "phonetic_hint": "Gud ívning", "category": "saudações", "owner": None, "language": "en"},
    {"front_pt": "Tchau / Até mais", "back_target": "Bye / See you", "phonetic_hint": "Bái / Sí iú", "category": "saudações", "owner": None, "language": "en"},
    {"front_pt": "Obrigado", "back_target": "Thank you", "phonetic_hint": "Ténk iú", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "Por favor", "back_target": "Please", "phonetic_hint": "Plíz", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "De nada", "back_target": "You're welcome", "phonetic_hint": "Iór uélcam", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "Desculpe / Com licença", "back_target": "Sorry / Excuse me", "phonetic_hint": "Sóri / Eks-kiúz mi", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "Você fala português?", "back_target": "Do you speak Portuguese?", "phonetic_hint": "Du iú spík pórtchu-guíz?", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "Eu não entendo", "back_target": "I don't understand", "phonetic_hint": "Ai dont ander-sténd", "category": "básico", "owner": None, "language": "en"},
    {"front_pt": "Pode me ajudar?", "back_target": "Can you help me?", "phonetic_hint": "Cén iú rélp mi?", "category": "básico", "owner": None, "language": "en"},

    # Conversa
    {"front_pt": "Pode falar mais devagar?", "back_target": "Could you speak more slowly?", "phonetic_hint": "Cud iú spík mór slôuli?", "category": "conversa", "owner": None, "language": "en"},
    {"front_pt": "Como se diz ... em inglês?", "back_target": "How do you say ... in English?", "phonetic_hint": "Ráu du iú sêi ... in ínglish?", "category": "conversa", "owner": None, "language": "en"},
    {"front_pt": "De onde você é?", "back_target": "Where are you from?", "phonetic_hint": "Uér ar iú fram?", "category": "conversa", "owner": None, "language": "en"},
    {"front_pt": "Eu sou do Brasil", "back_target": "I'm from Brazil", "phonetic_hint": "Aim fram bra-zíl", "category": "conversa", "owner": None, "language": "en"},
    {"front_pt": "Estou aprendendo inglês", "back_target": "I'm learning English", "phonetic_hint": "Aim lérning ínglish", "category": "conversa", "owner": None, "language": "en"},
    {"front_pt": "Prazer em conhecer você", "back_target": "Nice to meet you", "phonetic_hint": "Náis tu mít iú", "category": "conversa", "owner": None, "language": "en"},

    # Aeroporto
    {"front_pt": "Aqui está meu passaporte", "back_target": "Here is my passport", "phonetic_hint": "Ríar iz mai pás-port", "category": "aeroporto", "owner": None, "language": "en"},
    {"front_pt": "Estou aqui a turismo", "back_target": "I'm here on vacation", "phonetic_hint": "Aim ríar on vei-kêixon", "category": "aeroporto", "owner": None, "language": "en"},
    {"front_pt": "Onde fica o portão 12?", "back_target": "Where is gate 12?", "phonetic_hint": "Uér iz guêit tuélv?", "category": "aeroporto", "owner": None, "language": "en"},
    {"front_pt": "Perdi minha conexão", "back_target": "I missed my connection", "phonetic_hint": "Ai mist mai co-nékxon", "category": "aeroporto", "owner": None, "language": "en"},
    {"front_pt": "Só tenho bagagem de mão", "back_target": "I only have carry-on", "phonetic_hint": "Ai ônli rév kéri-on", "category": "aeroporto", "owner": None, "language": "en"},

    # Restaurante e compras
    {"front_pt": "Uma mesa para dois", "back_target": "A table for two", "phonetic_hint": "A têibol for tú", "category": "restaurante", "owner": None, "language": "en"},
    {"front_pt": "O cardápio, por favor", "back_target": "The menu, please", "phonetic_hint": "Dâ mêniu, plíz", "category": "restaurante", "owner": None, "language": "en"},
    {"front_pt": "A conta, por favor", "back_target": "The check, please", "phonetic_hint": "Dâ tchék, plíz", "category": "restaurante", "owner": None, "language": "en"},
    {"front_pt": "Quanto custa isso?", "back_target": "How much is this?", "phonetic_hint": "Ráu match iz dis?", "category": "compras", "owner": None, "language": "en"},
    {"front_pt": "Vocês aceitam cartão?", "back_target": "Do you take card?", "phonetic_hint": "Du iú têik card?", "category": "compras", "owner": None, "language": "en"},

    # Saúde
    {"front_pt": "Preciso de um médico", "back_target": "I need a doctor", "phonetic_hint": "Ai níd a dóctor", "category": "saúde", "owner": None, "language": "en"},
    {"front_pt": "Estou me sentindo mal", "back_target": "I don't feel well", "phonetic_hint": "Ai dont fíl uél", "category": "saúde", "owner": None, "language": "en"},
    {"front_pt": "Sou alérgico a ...", "back_target": "I'm allergic to ...", "phonetic_hint": "Aim a-lérdjic tu ...", "category": "saúde", "owner": "gabriela", "language": "en"},

    # Trabalho e moradia
    {"front_pt": "Tenho uma reunião às dez", "back_target": "I have a meeting at ten", "phonetic_hint": "Ai rév a míting at tén", "category": "trabalho", "owner": "ivan", "language": "en"},
    {"front_pt": "Podemos remarcar?", "back_target": "Can we reschedule?", "phonetic_hint": "Cén uí ri-skédiul?", "category": "trabalho", "owner": None, "language": "en"},
    {"front_pt": "Procuro um apartamento", "back_target": "I'm looking for an apartment", "phonetic_hint": "Aim lúking for an a-pártment", "category": "moradia", "owner": None, "language": "en"},
    {"front_pt": "Qual é o valor do aluguel?", "back_target": "How much is the rent?", "phonetic_hint": "Ráu match iz dâ rént?", "category": "moradia", "owner": None, "language": "en"},

    # Transporte
    {"front_pt": "À esquerda / à direita / em frente", "back_target": "left / right / straight ahead", "phonetic_hint": "left / rait / strêit a-réd", "category": "transporte", "owner": None, "language": "en"},
    {"front_pt": "Onde fica o banheiro?", "back_target": "Where is the restroom?", "phonetic_hint": "Uér iz dâ rést-rum?", "category": "transporte", "owner": None, "language": "en"},
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
                "speaker_target": "Guten Tag. Was kann ich für Sie tun?",
                "speaker_pt": "Bom dia. O que posso fazer pelo senhor?",
                "options": [
                    {"text_target": "Ich möchte mich anmelden.", "correct": True,
                     "explanation": "'sich anmelden' é o verbo exato para registrar o endereço — é a frase que o funcionário espera ouvir."},
                    {"text_target": "Ich will ein Konto.", "correct": False,
                     "explanation": "Isso é para abrir conta em banco; não tem relação com o registro de endereço."},
                    {"text_target": "Ich bin neu hier.", "correct": False,
                     "explanation": "Gramaticalmente ok, mas vago; o funcionário ainda precisaria perguntar o que você quer fazer."},
                ],
            },
            {
                "speaker_target": "Haben Sie die Wohnungsgeberbestätigung dabei?",
                "speaker_pt": "O senhor trouxe a confirmação do locador?",
                "options": [
                    {"text_target": "Ja, hier bitte.", "correct": True,
                     "explanation": "'hier bitte' é a forma natural de entregar um documento em alemão."},
                    {"text_target": "Was ist das?", "correct": False,
                     "explanation": "Esse documento é obrigatório para o registro; sem ele o atendimento não continua."},
                    {"text_target": "Nein, ich habe es vergessen.", "correct": False,
                     "explanation": "Sem a confirmação do locador não dá para concluir o Anmeldung — você teria que voltar outro dia."},
                ],
            },
            {
                "speaker_target": "Alles in Ordnung. Möchten Sie eine Meldebescheinigung?",
                "speaker_pt": "Está tudo certo. O senhor quer um comprovante de registro?",
                "options": [
                    {"text_target": "Ja, gerne.", "correct": True,
                     "explanation": "A Meldebescheinigung é exigida para abrir conta, contrato de celular etc. 'Ja, gerne' é a resposta educada padrão."},
                    {"text_target": "Nein, danke.", "correct": False,
                     "explanation": "Não é errado, mas você vai precisar desse comprovante logo em seguida."},
                    {"text_target": "Ich weiß nicht.", "correct": False,
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
                "speaker_target": "Guten Tag, wie kann ich Ihnen helfen?",
                "speaker_pt": "Bom dia, como posso ajudar?",
                "options": [
                    {"text_target": "Ich möchte ein Girokonto eröffnen.", "correct": True,
                     "explanation": "'Girokonto' é a conta do dia a dia e 'eröffnen' é o verbo certo para abrir conta."},
                    {"text_target": "Ich möchte Geld.", "correct": False,
                     "explanation": "Soa abrupto e não diz o que você quer fazer."},
                    {"text_target": "Haben Sie Konten?", "correct": False,
                     "explanation": "Pergunta estranha — obviamente o banco tem contas. Diga diretamente o que precisa."},
                ],
            },
            {
                "speaker_target": "Haben Sie einen Ausweis und eine Meldebescheinigung dabei?",
                "speaker_pt": "O senhor trouxe um documento de identidade e o comprovante de registro?",
                "options": [
                    {"text_target": "Ja, meinen Reisepass und die Meldebescheinigung.", "correct": True,
                     "explanation": "Dizer quais documentos você tem agiliza o processo e mostra preparo."},
                    {"text_target": "Nur meinen Pass.", "correct": False,
                     "explanation": "Sem a Meldebescheinigung a maioria dos bancos não abre a conta."},
                    {"text_target": "Ich habe einen Führerschein.", "correct": False,
                     "explanation": "A carteira de motorista brasileira normalmente não é aceita como identidade no banco."},
                ],
            },
            {
                "speaker_target": "Möchten Sie auch eine Kreditkarte?",
                "speaker_pt": "O senhor também quer um cartão de crédito?",
                "options": [
                    {"text_target": "Nein, eine Girocard reicht mir erstmal.", "correct": True,
                     "explanation": "A Girocard (débito) cobre o essencial na Alemanha; recusar com 'reicht mir erstmal' é natural."},
                    {"text_target": "Ja, alles.", "correct": False,
                     "explanation": "Aceitar tudo sem perguntar taxas pode gerar uma anuidade desnecessária."},
                    {"text_target": "Was ist eine Kreditkarte?", "correct": False,
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
                "speaker_target": "Schön, dass Sie da sind. Haben Sie Fragen zur Wohnung?",
                "speaker_pt": "Que bom que veio. Tem perguntas sobre o apartamento?",
                "options": [
                    {"text_target": "Ja, sind die Nebenkosten im Preis enthalten?", "correct": True,
                     "explanation": "Os 'Nebenkosten' (água, aquecimento) são decisivos no orçamento — é a primeira pergunta que um alemão faria."},
                    {"text_target": "Ist die Wohnung schön?", "correct": False,
                     "explanation": "Pergunta subjetiva demais; você está no local, forme sua própria opinião."},
                    {"text_target": "Warum ziehen die Vormieter aus?", "correct": False,
                     "explanation": "Pode soar intrusivo num primeiro contato; deixe para depois se for relevante."},
                ],
            },
            {
                "speaker_target": "Wie sieht es mit Ihrem Einkommen aus?",
                "speaker_pt": "Como está a sua situação de renda?",
                "options": [
                    {"text_target": "Ich habe einen unbefristeten Arbeitsvertrag und kann eine Gehaltsabrechnung zeigen.", "correct": True,
                     "explanation": "Contrato por tempo indeterminado + holerite é exatamente o que o locador quer ouvir para reduzir o risco."},
                    {"text_target": "Das geht Sie nichts an.", "correct": False,
                     "explanation": "Recusar responder praticamente elimina suas chances; comprovação de renda é padrão na Alemanha."},
                    {"text_target": "Ich verdiene genug.", "correct": False,
                     "explanation": "Vago; o locador precisa de números e documentos, não de garantias verbais."},
                ],
            },
            {
                "speaker_target": "Wann könnten Sie einziehen?",
                "speaker_pt": "Quando o senhor poderia se mudar?",
                "options": [
                    {"text_target": "Zum Ersten des nächsten Monats.", "correct": True,
                     "explanation": "Mudanças na Alemanha quase sempre começam no dia 1º do mês; a resposta soa organizada."},
                    {"text_target": "Irgendwann.", "correct": False,
                     "explanation": "Falta de compromisso passa a impressão de candidato pouco confiável."},
                    {"text_target": "Sofort, heute noch.", "correct": False,
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
                "speaker_target": "Guten Tag, was fehlt Ihnen?",
                "speaker_pt": "Bom dia, o que o senhor tem?",
                "options": [
                    {"text_target": "Ich habe seit gestern Halsschmerzen.", "correct": True,
                     "explanation": "'seit gestern' + o sintoma exato é o que o médico precisa para começar. Direto ao ponto."},
                    {"text_target": "Mir geht es nicht gut.", "correct": False,
                     "explanation": "Verdadeiro, mas vago; o médico teria que perguntar tudo de novo."},
                    {"text_target": "Ich brauche Medikamente.", "correct": False,
                     "explanation": "Quem decide isso é o médico; primeiro descreva o sintoma."},
                ],
            },
            {
                "speaker_target": "Haben Sie auch Fieber?",
                "speaker_pt": "O senhor também está com febre?",
                "options": [
                    {"text_target": "Ja, 38 Grad heute Morgen.", "correct": True,
                     "explanation": "Responder com o número mostra que você mediu — informação útil e objetiva."},
                    {"text_target": "Vielleicht.", "correct": False,
                     "explanation": "'Talvez' não ajuda o diagnóstico; se não sabe, diga que não mediu."},
                    {"text_target": "Ich hasse Fieber.", "correct": False,
                     "explanation": "Comentário pessoal fora de contexto."},
                ],
            },
            {
                "speaker_target": "Ich verschreibe Ihnen etwas. Sind Sie gegen Penicillin allergisch?",
                "speaker_pt": "Vou receitar um remédio. O senhor é alérgico a penicilina?",
                "options": [
                    {"text_target": "Nein, ich vertrage Penicillin.", "correct": True,
                     "explanation": "Confirmar a ausência de alergia com 'ich vertrage' é a formulação padrão."},
                    {"text_target": "Keine Ahnung.", "correct": False,
                     "explanation": "Alergia a antibiótico é sério; se não sabe, diga que nunca tomou — não deixe no ar."},
                    {"text_target": "Ja, aber das ist egal.", "correct": False,
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
                "speaker_target": "Kann ich Ihnen helfen?",
                "speaker_pt": "Posso ajudar?",
                "options": [
                    {"text_target": "Ja, wo finde ich Joghurt?", "correct": True,
                     "explanation": "'Wo finde ich...?' é a pergunta padrão para localizar um produto."},
                    {"text_target": "Ich suche etwas.", "correct": False,
                     "explanation": "Vago demais; diga o que procura."},
                    {"text_target": "Haben Sie Joghurt?", "correct": False,
                     "explanation": "O supermercado obviamente tem; a dúvida é onde, não se tem."},
                ],
            },
            {
                "speaker_target": "Der ist im Kühlregal, Gang 4. Sonst noch etwas?",
                "speaker_pt": "Fica na geladeira, corredor 4. Mais alguma coisa?",
                "options": [
                    {"text_target": "Nein danke, das war's.", "correct": True,
                     "explanation": "'das war's' encerra a interação de forma natural."},
                    {"text_target": "Ich weiß nicht.", "correct": False,
                     "explanation": "Indecisão trava a conversa; se acabou, diga que acabou."},
                    {"text_target": "Warum Gang 4?", "correct": False,
                     "explanation": "Questionar a localização não faz sentido; agradeça e vá."},
                ],
            },
            {
                "speaker_target": "Zusammen 12,40 Euro. Zahlen Sie mit Karte?",
                "speaker_pt": "Dá 12,40 no total. Vai pagar com cartão?",
                "options": [
                    {"text_target": "Ja, mit Karte, bitte.", "correct": True,
                     "explanation": "Resposta direta; muitos caixas menores preferem saber antes de finalizar."},
                    {"text_target": "Ich habe nur einen großen Schein.", "correct": False,
                     "explanation": "Não responde à pergunta; diga cartão ou dinheiro primeiro."},
                    {"text_target": "Ist das nicht zu teuer?", "correct": False,
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
                "speaker_target": "Guten Morgen, was darf's sein?",
                "speaker_pt": "Bom dia, o que vai ser?",
                "options": [
                    {"text_target": "Zwei Brötchen und einen Kaffee zum Mitnehmen, bitte.", "correct": True,
                     "explanation": "Quantidade + item + 'zum Mitnehmen' (para viagem) numa frase só — exatamente o esperado."},
                    {"text_target": "Was haben Sie?", "correct": False,
                     "explanation": "Perguntar o cardápio inteiro numa fila de manhã é pouco prático; olhe a vitrine."},
                    {"text_target": "Ich will Brot.", "correct": False,
                     "explanation": "'Ich will' soa rude e 'Brot' sem quantidade obriga outra pergunta."},
                ],
            },
            {
                "speaker_target": "Möchten Sie die Brötchen aufgeschnitten?",
                "speaker_pt": "Quer os pãezinhos cortados?",
                "options": [
                    {"text_target": "Nein danke, so ist gut.", "correct": True,
                     "explanation": "'so ist gut' é a forma natural de recusar educadamente."},
                    {"text_target": "Was heißt aufgeschnitten?", "correct": False,
                     "explanation": "Trava a fila; nesse caso um simples 'ja' ou 'nein' resolve."},
                    {"text_target": "Egal.", "correct": False,
                     "explanation": "'Tanto faz' soa desinteressado; dê uma resposta clara."},
                ],
            },
            {
                "speaker_target": "Das macht 4,20 Euro.",
                "speaker_pt": "Dá 4,20 euros.",
                "options": [
                    {"text_target": "Hier, bitte. Stimmt so.", "correct": True,
                     "explanation": "Entregar o dinheiro com 'stimmt so' (pode ficar com o troco) é padrão em valores pequenos."},
                    {"text_target": "Ich zahle mit einer 50.", "correct": False,
                     "explanation": "Nota grande para compra pequena irrita; tenha trocado ou pague com cartão."},
                    {"text_target": "So teuer?", "correct": False,
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
                "speaker_target": "Praxis Dr. Weber, guten Tag.",
                "speaker_pt": "Consultório Dr. Weber, bom dia.",
                "options": [
                    {"text_target": "Guten Tag, ich möchte einen Termin vereinbaren.", "correct": True,
                     "explanation": "'einen Termin vereinbaren' é a fórmula exata para marcar consulta."},
                    {"text_target": "Ich bin krank.", "correct": False,
                     "explanation": "Direto demais e não diz o que você quer da ligação."},
                    {"text_target": "Sind Sie der Arzt?", "correct": False,
                     "explanation": "Você ligou para a recepção; pergunta desnecessária."},
                ],
            },
            {
                "speaker_target": "Waren Sie schon einmal bei uns?",
                "speaker_pt": "O senhor já foi atendido aqui antes?",
                "options": [
                    {"text_target": "Nein, ich bin neu und gesetzlich versichert.", "correct": True,
                     "explanation": "Dizer que é novo + o tipo de plano (gesetzlich/privat) adianta o cadastro."},
                    {"text_target": "Ich glaube nicht.", "correct": False,
                     "explanation": "Ou você já foi ou não; a recepção precisa de certeza."},
                    {"text_target": "Ist das wichtig?", "correct": False,
                     "explanation": "É sim — muda o cadastro e os horários disponíveis."},
                ],
            },
            {
                "speaker_target": "Wir haben einen Termin am Donnerstag um 9 Uhr. Passt das?",
                "speaker_pt": "Temos um horário na quinta às 9h. Serve?",
                "options": [
                    {"text_target": "Ja, das passt. Vielen Dank.", "correct": True,
                     "explanation": "Confirmar com 'das passt' e agradecer fecha a ligação de forma limpa."},
                    {"text_target": "Vielleicht.", "correct": False,
                     "explanation": "A recepção precisa reservar ou liberar o horário; responda sim ou não."},
                    {"text_target": "Donnerstag ist schlecht, aber egal.", "correct": False,
                     "explanation": "Contradição: se não serve, diga e peça outro horário — aceitar 'de qualquer jeito' gera falta."},
                ],
            },
        ],
    },

    # ----------------------------------------------------------------------- #
    # Cenários de inglês                                                      #
    # ----------------------------------------------------------------------- #
    {
        "slug": "airport-check-in",
        "title": "Check-in no aeroporto",
        "description": (
            "Você chega ao balcão de check-in para um voo internacional. Tenha o "
            "passaporte e a reserva à mão."
        ),
        "category": "viagem",
        "language": "en",
        "steps": [
            {
                "speaker_target": "Good morning. May I see your passport and booking, please?",
                "speaker_pt": "Bom dia. Posso ver seu passaporte e a reserva, por favor?",
                "options": [
                    {"text_target": "Here you are.", "correct": True,
                     "explanation": "'Here you are' é a forma natural de entregar um documento em inglês."},
                    {"text_target": "Why do you need it?", "correct": False,
                     "explanation": "O passaporte é obrigatório no check-in internacional; questionar só atrasa."},
                    {"text_target": "I forgot it at home.", "correct": False,
                     "explanation": "Sem passaporte não há embarque — você não conseguiria seguir."},
                ],
            },
            {
                "speaker_target": "Are you checking any bags today?",
                "speaker_pt": "Você vai despachar alguma mala hoje?",
                "options": [
                    {"text_target": "No, I only have carry-on.", "correct": True,
                     "explanation": "Responde a pergunta e adianta o atendimento com a informação que o agente precisa."},
                    {"text_target": "Maybe later.", "correct": False,
                     "explanation": "A bagagem é despachada agora, no balcão; não dá para deixar para depois."},
                    {"text_target": "I don't like bags.", "correct": False,
                     "explanation": "Fora de contexto — o agente só quer saber se há mala a despachar."},
                ],
            },
            {
                "speaker_target": "Would you like a window or an aisle seat?",
                "speaker_pt": "Você prefere janela ou corredor?",
                "options": [
                    {"text_target": "An aisle seat, please.", "correct": True,
                     "explanation": "Escolha objetiva e educada com 'please' — exatamente o que o agente espera."},
                    {"text_target": "I don't care.", "correct": False,
                     "explanation": "Soa rude; se não tiver preferência, diga 'either is fine'."},
                    {"text_target": "Where is the plane?", "correct": False,
                     "explanation": "Não responde à pergunta sobre o assento."},
                ],
            },
        ],
    },
    {
        "slug": "job-interview",
        "title": "Entrevista de emprego",
        "description": (
            "Primeira conversa com o recrutador de uma empresa de tecnologia. "
            "Respostas curtas, concretas e com exemplos funcionam melhor."
        ),
        "category": "trabalho",
        "language": "en",
        "steps": [
            {
                "speaker_target": "Thanks for coming in. Can you tell me a bit about yourself?",
                "speaker_pt": "Obrigado por vir. Pode falar um pouco sobre você?",
                "options": [
                    {"text_target": "Sure. I've worked as a database administrator for five years and I'm moving into backend development.",
                     "correct": True,
                     "explanation": "Resposta focada na carreira e no objetivo — é o que o recrutador quer ouvir nessa pergunta."},
                    {"text_target": "What do you want to know?", "correct": False,
                     "explanation": "Devolve a pergunta em vez de responder; passa insegurança."},
                    {"text_target": "It's all on my CV.", "correct": False,
                     "explanation": "Soa desinteressado; a pergunta é a sua chance de se apresentar."},
                ],
            },
            {
                "speaker_target": "Why do you want to work here?",
                "speaker_pt": "Por que você quer trabalhar aqui?",
                "options": [
                    {"text_target": "I like that your team ships small changes often and values clean code.",
                     "correct": True,
                     "explanation": "Mostra que você pesquisou a empresa e conecta com o que você valoriza."},
                    {"text_target": "I need a job.", "correct": False,
                     "explanation": "Honesto, mas não dá nenhum motivo para escolherem você."},
                    {"text_target": "The salary is good.", "correct": False,
                     "explanation": "Dinheiro pode importar, mas sozinho não é uma resposta forte numa entrevista."},
                ],
            },
            {
                "speaker_target": "Do you have any questions for us?",
                "speaker_pt": "Você tem alguma pergunta para nós?",
                "options": [
                    {"text_target": "Yes — what does the first month look like for a new developer?",
                     "correct": True,
                     "explanation": "Uma pergunta específica sobre o dia a dia mostra interesse real na vaga."},
                    {"text_target": "No, I'm good.", "correct": False,
                     "explanation": "Perde a chance de demonstrar interesse; quase sempre vale ter uma pergunta pronta."},
                    {"text_target": "Can I go now?", "correct": False,
                     "explanation": "Soa impaciente e encerra a entrevista de forma ruim."},
                ],
            },
        ],
    },
    {
        "slug": "doctor-visit",
        "title": "Consulta médica",
        "description": (
            "Você vai ao médico com uma dor de garganta que começou ontem. "
            "Descreva os sintomas com clareza."
        ),
        "category": "saúde",
        "language": "en",
        "steps": [
            {
                "speaker_target": "What brings you in today?",
                "speaker_pt": "O que traz você aqui hoje?",
                "options": [
                    {"text_target": "I've had a sore throat since yesterday.", "correct": True,
                     "explanation": "Sintoma + quando começou: exatamente a informação que o médico precisa primeiro."},
                    {"text_target": "I feel bad.", "correct": False,
                     "explanation": "Vago demais; o médico teria que perguntar tudo de novo."},
                    {"text_target": "I need antibiotics.", "correct": False,
                     "explanation": "Pedir o remédio antes do exame; deixe o médico avaliar."},
                ],
            },
            {
                "speaker_target": "Do you have a fever?",
                "speaker_pt": "Você está com febre?",
                "options": [
                    {"text_target": "Yes, 38 degrees this morning.", "correct": True,
                     "explanation": "Confirma e dá um número — ajuda o médico a medir a gravidade."},
                    {"text_target": "I think so.", "correct": False,
                     "explanation": "Impreciso; se não mediu, diga 'I haven't checked'."},
                    {"text_target": "Fever is the worst.", "correct": False,
                     "explanation": "Comentário sem informação; não responde à pergunta."},
                ],
            },
            {
                "speaker_target": "I'll prescribe something. Are you allergic to penicillin?",
                "speaker_pt": "Vou receitar algo. Você é alérgico a penicilina?",
                "options": [
                    {"text_target": "No, I can take penicillin.", "correct": True,
                     "explanation": "Resposta clara sobre alergia — informação de segurança essencial antes da receita."},
                    {"text_target": "No idea.", "correct": False,
                     "explanation": "Se não sabe, diga isso de forma completa; 'no idea' é seco e pouco útil."},
                    {"text_target": "Yes, but it's fine.", "correct": False,
                     "explanation": "Contradição perigosa: uma alergia relatada muda totalmente a receita."},
                ],
            },
        ],
    },
]
