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

no_title_json = {
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
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

no_participants_json = {
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

no_messages_json = {
    "participants": [
        {
            "name": "Jessica Zhang"
        },
        {
            "name": "Jeff Lai"
        }
    ],
    "title": "Jessica Zhang",
    "is_still_participant": True,
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

no_is_still_participant_json = {
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
    "thread_type": "Regular",
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

no_thread_type_json = {
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
    "thread_path": "inbox/JessicaZhang_Zs11Uy-bpw"
}

no_thread_path_json = {
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
}

no_name_array = [
    {
      "name": "Jessica Zhang"
    },
    {
      "no_name": "Jeff Lai"
    }
]

no_reaction_array = [
        {
          "no_reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ]

no_actor_array = [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "no_actor": "Jeff Lai"
        }
      ]
no_reaction_in_messages_array = [
    {
      "sender_name": "Jessica Zhang",
      "timestamp_ms": 1565582588971,
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "reactions": [
        {
          "no_reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
      "type": "Generic"
    }
  ]
no_sender_name_array = [
    {
      "timestamp_ms": 1565582588971,
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
      "type": "Generic"
    }
  ]

no_timestamp_ms_array = [
    {
      "sender_name": "Jessica Zhang",
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
      "type": "Generic"
    }
  ]

no_content_array = [
    {
      "sender_name": "Jessica Zhang",
      "timestamp_ms": 1565582588971,
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
      "type": "Generic"
    }
  ]

no_reactions_array = [
    {
      "sender_name": "Jessica Zhang",
      "timestamp_ms": 1565582588971,
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "type": "Generic"
    }
  ]

no_type_array = [
    {
      "sender_name": "Jessica Zhang",
      "timestamp_ms": 1565582588971,
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
    }
  ]

returned_json_data = {
  "participants": [
    {
      "name": "Jessica Zhang"
    },
    {
      "name": "\u00f0\u009f\u0098\u0086Jeff Lai"
    }
  ],
  "messages": [
    {
      "sender_name": "Jessica Zhang",
      "timestamp_ms": 1565582588971,
      "content": "It\u00e2\u0080\u0099s up to the 220 gods now",
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jeff Lai"
        }
      ],
      "type": "Generic"
    }
  ],
  "title": "\u00f0\u009f\u0098\u0086Jessica Zhang",
  "is_still_participant": True,
  "thread_type": "Regular",
  "thread_path": "\u00f0\u009f\u0098\u0086inbox/JessicaZhang_Zs11Uy-bpw"
}