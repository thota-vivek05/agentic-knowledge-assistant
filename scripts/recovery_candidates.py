RECOVERY_CANDIDATES = [
    {
        "question": (
            "What mechanism lets TCP cautiously probe "
            "how much capacity the network can handle?"
        ),
        "target_concept": "slow start",
    },
    {
        "question": (
            "How does TCP react when it discovers that "
            "the network cannot handle the current sending rate?"
        ),
        "target_concept": "TCP reaction to congestion",
    },
    {
        "question": (
            "How does TCP gradually increase its sending rate "
            "after congestion has been reduced?"
        ),
        "target_concept": "congestion avoidance",
    },
    {
        "question": (
            "What strategy does TCP use to increase its transmission "
            "rate while reducing it when congestion appears?"
        ),
        "target_concept": "additive increase multiplicative decrease",
    },
    {
        "question": (
            "How does TCP change its congestion window after "
            "detecting packet loss?"
        ),
        "target_concept": "packet loss",
    },
    {
        "question": (
            "What are the different stages TCP uses to control "
            "congestion in the network?"
        ),
        "target_concept": "TCP congestion control phases",
    },
]