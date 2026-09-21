# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2026/9/21
# @FileName: test_memory_util_message_forms.py
import unittest

from agentuniverse.agent.memory.message import Message
from agentuniverse.base.util.memory_util import generate_messages, get_memory_string


class TestGetMemoryStringMessageForms(unittest.TestCase):
    """get_memory_string must accept the same message forms as
    generate_messages (str / dict / Message), since callers pass raw
    chat_history lists straight through (AgentTemplate.process_memory)."""

    def test_dict_elements_are_rendered(self):
        result = get_memory_string([{'type': 'human', 'content': 'hi'}], 'agent1')
        self.assertIn('hi', result)

    def test_str_elements_are_rendered(self):
        result = get_memory_string(['hello'], 'agent1')
        self.assertIn('hello', result)

    def test_output_typed_message_without_trace_id_is_rendered(self):
        message = Message(type='output', content='the answer', metadata={})
        result = get_memory_string([message], 'agent1')
        self.assertIn('the answer', result)

    def test_current_trace_messages_are_still_skipped(self):
        from unittest import mock

        from agentuniverse.agent.memory.conversation_memory.conversation_message import \
            ConversationMessage

        message = ConversationMessage(type='output', content='current turn',
                                      metadata={}, trace_id='trace-1')
        with mock.patch(
                'agentuniverse.base.util.memory_util.FrameworkContextManager'
        ) as context_manager_cls:
            context_manager_cls.return_value.get_context.return_value = 'trace-1'
            result = get_memory_string([message], 'agent1')
        self.assertEqual('', result)

    def test_generate_messages_contract_is_unchanged(self):
        messages = generate_messages(['plain', {'type': 'human', 'content': 'hi'}])
        self.assertEqual([Message, Message], [type(m) for m in messages])


if __name__ == '__main__':
    unittest.main()
