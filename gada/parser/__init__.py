__all__ = ["parse_type"]
from antlr4 import *
from .dist.GadaLexer import GadaLexer
from .dist.GadaParser import GadaParser
from .dist.GadaVisitor import GadaVisitor
from gada import typing
from gada._log import logger


class Visitor(GadaVisitor):
    def visitChunk(self, ctx: GadaParser.ChunkContext):
        return self.visit(ctx.block())

    def visitBlock(self, ctx: GadaParser.BlockContext):
        return self.visit(ctx.typeUnion())

    def visitTypeUnion(self, ctx: GadaParser.TypeUnionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.type_(0))

        return typing.UnionType(map(self.visit, ctx.type_()))

    def visitTypeList(self, ctx: GadaParser.TypeListContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.type_(0))

        return map(self.visit, ctx.type_())

    def visitType(self, ctx: GadaParser.TypeContext):
        if ctx.name:
            return {
                "int": typing.IntType(),
                "float": typing.FloatType(),
                "str": typing.StringType(),
                "bool": typing.BoolType(),
            }[ctx.name.text]

        if ctx.operator.text == "[":
            return typing.ListType(self.visit(ctx.listItem) if ctx.listItem else None)

        return typing.TupleType(self.visit(ctx.tupleItem))


def type(s: str, /) -> typing.Type:
    r'''Parse the textual representation of a type.
    
    .. code-block:: python

        >>> from gada import parser
        >>> parser.type('bool')
        BoolType()
        >>> parser.type('int')
        IntType()
        >>> parser.type('float')
        FloatType()
        >>> parser.type('str')
        StringType()
        >>> parser.type('[int]')
        ListType(IntType())
        >>> parser.type('(int, str)')
        TupleType([IntType(), StringType()])
        >>>
    
    :param s: textual representation
    :return: type
    '''
    # lexer
    lexer = GadaLexer(InputStream(s))
    stream = CommonTokenStream(lexer)
    # parser
    parser = GadaParser(stream)
    tree = parser.typeUnion()
    # evaluator
    visitor = Visitor()
    return visitor.visit(tree)
