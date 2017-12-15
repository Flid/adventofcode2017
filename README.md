## Advent Of Code 2017 solutiuons

That's my approach to solve the [tasks](https://adventofcode.com/2017). It's not funny to use usual programming languages, so I decided to learn something new. I'd like to try at least 15 languages, including something extream like FPGA development.

## Languages used:

1. Lucid/Verilog (1)
2. Lucid/Verilog
3. Lucid/Verilog
4. Ruby
5. C
6. C++11
7. Scala
8. Erlang
9. Java

(1) Lucid is an extension for Verilog, Hardware Description Language, I've uploaded it to a real FPGA, the data being sent using a Python script.

## Requirements

All FPGA solutions receive data via serial port in a [special format](https://embeddedmicro.com/tutorials/lucid/register-interface-tutorial), so I wrote a [small library](https://github.com/Flid/pymojolib) to interact with my Mojo V3 board.
