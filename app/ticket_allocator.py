"""
This module contains a function that
handles ticket allocation among agents in
a roundrobin fashion.
"""
from typing import DefaultDict
import collections


def allocate_ticket(tickets: list, agents: list) -> DefaultDict:
    """
    :param: tickets - tickets to allocate
    :param: agents - agents to allocate tickets to
    :return: DefaultDict, a mapping of an agent to his or her tickets
    """
    allocated_tickets = collections.defaultdict(list)
    for i, ticket in enumerate(tickets):
        agent = agents[i % len(agents)]
        allocated_tickets[agent].append(ticket)
    return allocated_tickets
