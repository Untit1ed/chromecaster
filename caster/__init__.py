
from caster._caster import Caster
from parsers import fallback, tube, web, abstract_parser


def get_parser_for_url(url) -> list[abstract_parser.AbstractParser]:
    '''
    Gets a suitable parser for a url
    '''
    parsers = get_parsers()

    parser_map = {}
    for parser in parsers:
        for domain in parser.supported_domains():
            if domain not in parser_map:
                parser_map[domain] = []
            parser_map[domain].append(parser)

    for domain, parsers in parser_map.items():
        if domain in url:
            return parsers

    return [fallback.FallbackParser]


def get_parsers() -> list[abstract_parser.AbstractParser]:
    '''
    Gets a list of available parsers
    '''
    return [tube.TubeParser,web.WebParser]
