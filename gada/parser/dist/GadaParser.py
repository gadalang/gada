# Generated from .\Gada.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,47,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,0,1,
        1,1,1,1,2,1,2,1,2,5,2,19,8,2,10,2,12,2,22,9,2,1,3,1,3,1,3,5,3,27,
        8,3,10,3,12,3,30,9,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,38,8,4,1,4,1,4,
        1,4,1,4,1,4,3,4,45,8,4,1,4,0,0,5,0,2,4,6,8,0,0,49,0,10,1,0,0,0,2,
        13,1,0,0,0,4,15,1,0,0,0,6,23,1,0,0,0,8,44,1,0,0,0,10,11,3,2,1,0,
        11,12,5,0,0,1,12,1,1,0,0,0,13,14,3,4,2,0,14,3,1,0,0,0,15,20,3,8,
        4,0,16,17,5,1,0,0,17,19,3,8,4,0,18,16,1,0,0,0,19,22,1,0,0,0,20,18,
        1,0,0,0,20,21,1,0,0,0,21,5,1,0,0,0,22,20,1,0,0,0,23,28,3,8,4,0,24,
        25,5,2,0,0,25,27,3,8,4,0,26,24,1,0,0,0,27,30,1,0,0,0,28,26,1,0,0,
        0,28,29,1,0,0,0,29,7,1,0,0,0,30,28,1,0,0,0,31,45,5,3,0,0,32,45,5,
        4,0,0,33,45,5,5,0,0,34,45,5,6,0,0,35,37,5,7,0,0,36,38,3,4,2,0,37,
        36,1,0,0,0,37,38,1,0,0,0,38,39,1,0,0,0,39,45,5,8,0,0,40,41,5,9,0,
        0,41,42,3,6,3,0,42,43,5,10,0,0,43,45,1,0,0,0,44,31,1,0,0,0,44,32,
        1,0,0,0,44,33,1,0,0,0,44,34,1,0,0,0,44,35,1,0,0,0,44,40,1,0,0,0,
        45,9,1,0,0,0,4,20,28,37,44
    ]

class GadaParser ( Parser ):

    grammarFileName = "Gada.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'|'", "','", "'int'", "'float'", "'str'", 
                     "'bool'", "'['", "']'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "NAME", "WS" ]

    RULE_chunk = 0
    RULE_block = 1
    RULE_typeUnion = 2
    RULE_typeList = 3
    RULE_type = 4

    ruleNames =  [ "chunk", "block", "typeUnion", "typeList", "type" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    NAME=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ChunkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(GadaParser.BlockContext,0)


        def EOF(self):
            return self.getToken(GadaParser.EOF, 0)

        def getRuleIndex(self):
            return GadaParser.RULE_chunk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChunk" ):
                listener.enterChunk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChunk" ):
                listener.exitChunk(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChunk" ):
                return visitor.visitChunk(self)
            else:
                return visitor.visitChildren(self)




    def chunk(self):

        localctx = GadaParser.ChunkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_chunk)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.block()
            self.state = 11
            self.match(GadaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeUnion(self):
            return self.getTypedRuleContext(GadaParser.TypeUnionContext,0)


        def getRuleIndex(self):
            return GadaParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = GadaParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self.typeUnion()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeUnionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GadaParser.TypeContext)
            else:
                return self.getTypedRuleContext(GadaParser.TypeContext,i)


        def getRuleIndex(self):
            return GadaParser.RULE_typeUnion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeUnion" ):
                listener.enterTypeUnion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeUnion" ):
                listener.exitTypeUnion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeUnion" ):
                return visitor.visitTypeUnion(self)
            else:
                return visitor.visitChildren(self)




    def typeUnion(self):

        localctx = GadaParser.TypeUnionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_typeUnion)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.type_()
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GadaParser.T__0:
                self.state = 16
                self.match(GadaParser.T__0)
                self.state = 17
                self.type_()
                self.state = 22
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GadaParser.TypeContext)
            else:
                return self.getTypedRuleContext(GadaParser.TypeContext,i)


        def getRuleIndex(self):
            return GadaParser.RULE_typeList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeList" ):
                listener.enterTypeList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeList" ):
                listener.exitTypeList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeList" ):
                return visitor.visitTypeList(self)
            else:
                return visitor.visitChildren(self)




    def typeList(self):

        localctx = GadaParser.TypeListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_typeList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.type_()
            self.state = 28
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GadaParser.T__1:
                self.state = 24
                self.match(GadaParser.T__1)
                self.state = 25
                self.type_()
                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token
            self.operator = None # Token
            self.listItem = None # TypeUnionContext
            self.tupleItem = None # TypeListContext

        def typeUnion(self):
            return self.getTypedRuleContext(GadaParser.TypeUnionContext,0)


        def typeList(self):
            return self.getTypedRuleContext(GadaParser.TypeListContext,0)


        def getRuleIndex(self):
            return GadaParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = GadaParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.state = 44
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GadaParser.T__2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                localctx.name = self.match(GadaParser.T__2)
                pass
            elif token in [GadaParser.T__3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                localctx.name = self.match(GadaParser.T__3)
                pass
            elif token in [GadaParser.T__4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                localctx.name = self.match(GadaParser.T__4)
                pass
            elif token in [GadaParser.T__5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 34
                localctx.name = self.match(GadaParser.T__5)
                pass
            elif token in [GadaParser.T__6]:
                self.enterOuterAlt(localctx, 5)
                self.state = 35
                localctx.operator = self.match(GadaParser.T__6)
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GadaParser.T__2) | (1 << GadaParser.T__3) | (1 << GadaParser.T__4) | (1 << GadaParser.T__5) | (1 << GadaParser.T__6) | (1 << GadaParser.T__8))) != 0):
                    self.state = 36
                    localctx.listItem = self.typeUnion()


                self.state = 39
                self.match(GadaParser.T__7)
                pass
            elif token in [GadaParser.T__8]:
                self.enterOuterAlt(localctx, 6)
                self.state = 40
                localctx.operator = self.match(GadaParser.T__8)
                self.state = 41
                localctx.tupleItem = self.typeList()
                self.state = 42
                self.match(GadaParser.T__9)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





