
grammar Gada;

chunk
    : block EOF
    ;

block
    : typeUnion
    ;

typeUnion
    : type ('|' type)*
    ;

typeList
    : type (',' type)*
    ;

type
    : name='int'
    | name='float'
    | name='str'
    | name='bool'
    | operator='[' listItem=typeUnion? ']'
    | operator='(' tupleItem=typeList ')'
    ;

// LEXER

NAME
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

WS
    : [ \t\u000C\r\n]+ -> skip
    ;
