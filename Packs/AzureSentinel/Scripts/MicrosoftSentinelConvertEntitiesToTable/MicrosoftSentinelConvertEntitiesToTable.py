import demistomock as demisto
from CommonServerPython import *
from itertools import chain
import ast


def format_entity(entity: dict) -> dict:
    """
    Converts an entity to a dictionary with the relevant fields.
    """
    return {
        'name': entity.get('name'),
        'kind': entity.get('kind'),
        **entity.get('properties', {})
    }


def convert_to_table(context_results: str) -> CommandResults:
    """
    Args:
        context_results (str): String representing a list of dicts

    Returns:
        CommandResults: CommandResults object containing only readable_output
    """
    context_results = re.sub(
        r':\s*(true|false)\b',
        lambda x: f':{x.group(1).capitalize()}',
        context_results
    )  # Convert true/false to True/False for literal_eval
    context_results = ast.literal_eval(context_results)

    context_formatted = [
        format_entity(entity) for entity in context_results
    ]

    md = tableToMarkdown(
        '',
        context_formatted,
        headers=[*dict.fromkeys(chain.from_iterable(context_formatted))],
        removeNull=True,
        sort_headers=False,
        headerTransform=pascalToSpace
    )

    return CommandResults(
        readable_output=md
    )


def main():
    context = dict_safe_get(
        demisto.callingContext,
        ['context', 'Incidents', 0, 'CustomFields', 'microsoftsentinelentities'],
        {}
    )

    if not context:
        return_error('No data to present')

    return_results(convert_to_table(context))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
