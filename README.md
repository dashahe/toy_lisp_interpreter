# toy_lisp_interpreter

This is a toy scheme interpreter written in python for practice. Some basic functions are available: 
- primitive  procedure and numbers
- if statement
- lambda expression
- definition of variable

It mainly contains two parts: `parser` and `evaluator`. Scheme is a special language and it's so easy to write the parser in python. As for the evaluator, we need `environment table` to implement application and variable declarations. So we use class `environment` to be  environment table. 

## example
basic calculator
```
Tiny Lisp> (* 2 (+ 1 1))
4
```


