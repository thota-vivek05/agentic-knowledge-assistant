EVALUATION_DATA = [
    # ------------------------------------------------------------
    # Direct questions
    # ------------------------------------------------------------
    {
        "question": "How does TCP slow start work?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What is TCP Tahoe?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What is TCP Reno?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What is congestion avoidance?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What is additive increase multiplicative decrease?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What happens when TCP detects packet loss?",
        "category": "direct",
        "expected_answered": True,
    },
    {
        "question": "What is explicit congestion notification?",
        "category": "direct",
        "expected_answered": True,
    },

    # ------------------------------------------------------------
    # Paraphrased questions
    # ------------------------------------------------------------
    {
        "question": "How does TCP increase its congestion window at the beginning?",
        "category": "paraphrased",
        "expected_answered": True,
    },
    {
        "question": "How does TCP detect and respond to congestion?",
        "category": "paraphrased",
        "expected_answered": True,
    },
    {
        "question": "How does TCP control its sending rate when the network is congested?",
        "category": "paraphrased",
        "expected_answered": True,
    },

    # ------------------------------------------------------------
    # Vague but supported questions
    # ------------------------------------------------------------
    {
        "question": "What happens when the network becomes congested?",
        "category": "vague",
        "expected_answered": True,
    },
    {
        "question": "How does TCP deal with congestion?",
        "category": "vague",
        "expected_answered": True,
    },
    {
        "question": "What does TCP do when things go wrong in the network?",
        "category": "vague",
        "expected_answered": True,
    },

    # ------------------------------------------------------------
    # Difficult / multi-concept questions
    # ------------------------------------------------------------
    {
        "question": "What are the phases of TCP congestion control?",
        "category": "difficult",
        "expected_answered": True,
    },
    {
        "question": "How do TCP Tahoe and TCP Reno respond to packet loss?",
        "category": "difficult",
        "expected_answered": True,
    },
    {
        "question": "How are slow start and congestion avoidance related?",
        "category": "difficult",
        "expected_answered": True,
    },

    # ------------------------------------------------------------
    # Out-of-scope questions
    # ------------------------------------------------------------
    {
        "question": "What is the capital of France?",
        "category": "out_of_scope",
        "expected_answered": False,
    },
    {
        "question": "Who invented the Python programming language?",
        "category": "out_of_scope",
        "expected_answered": False,
    },
    {
        "question": "What is the largest planet in the solar system?",
        "category": "out_of_scope",
        "expected_answered": False,
    },

    # ------------------------------------------------------------
    # Related but unsupported questions
    # ------------------------------------------------------------
    {
        "question": "What is TCP CUBIC?",
        "category": "related_unsupported",
        "expected_answered": False,
    },
    {
        "question": "How does TCP BBR work?",
        "category": "related_unsupported",
        "expected_answered": False,
    },
    {
        "question": "What is TCP New Reno?",
        "category": "related_unsupported",
        "expected_answered": False,
    },
]