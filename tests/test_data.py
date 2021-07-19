bad_sender_name_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test\u00e2\u0080\u0099",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "Jessica Zhang",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

good_sender_name_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test'",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "Jessica Zhang",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

bad_title_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "test\u00e2\u0080\u0099",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

good_title_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "test'",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

bad_emoji_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol\u00e2\u0080\u0099",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "test",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

good_emoji_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "messages": [
        {
            "sender_name": "test",
            "timestamp_ms": 1565582588971,
            "content": "Its up to the 220 gods now",
            "reactions": [
                {
                    "reaction": "lol'",
                    "actor": "Jeff Lai"
                }
            ],
            "type": "Generic"
        }
    ],
    "title": "test",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}
