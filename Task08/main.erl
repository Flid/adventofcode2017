-module(main). 
-export([main/0]). 

read_lines(FileName) ->
    {ok, Device} = file:open(FileName, [read]),
    try get_all_lines(Device)
      after file:close(Device)
    end.

get_ines(Device) ->
    case file:read_line(Device) of
        {ok, Data} -> [Data | get_all_lines(Device)];
        eof        -> []
    end.

    
is_condition_satisfied(Map, CondReg, Cond, CondVal) -> 
    CurrentCondVal = maps:get(CondReg, Map, 0),
    if 
      Cond == ">" -> CurrentCondVal > CondVal;
      Cond == "<" -> CurrentCondVal < CondVal;
      Cond == ">=" -> CurrentCondVal >= CondVal;
      Cond == "<=" -> CurrentCondVal =< CondVal;
      Cond == "==" -> CurrentCondVal == CondVal;
      Cond == "!=" -> CurrentCondVal /= CondVal
    end.
    

perform_action(Map, Reg, Op, Val) -> 
    CurrentVal = maps:get(Reg, Map, 0),
    io:format("Performing ~s operation~n", [Op]),
    if
      Op == "inc" -> maps:put(Reg, CurrentVal + Val, Map);
      Op == "dec" -> maps:put(Reg, CurrentVal - Val, Map)
    end.
    

get_max_value([], MaxVal) -> 
    MaxVal;
get_max_value([Val | Rest], MaxVal) -> 
    if
      Val > MaxVal -> get_max_value(Rest, Val);
      true -> get_max_value(Rest, MaxVal)
    end.

process_ine([], Map) ->
    MaxVal = get_max_value(maps:values(Map), 0),
    io:format("Max register value: ~B~n", [MaxVal]),
    ok;
process_line([Line | Rest], Map) ->
    [Reg, Op, ValStr, If, CondReg, Cond, CondValNL | NewLine] = string:tokens(Line, " "),
    {CondVal, _Rest} = string:to_integer(re:replace(CondValNL, "(^\\s+)|(\\s+$)", "", [global,{return,list}])),
    {Val, _Rest} = string:to_integer(ValStr),
    
    case is_condition_satisfied(Map, CondReg, Cond, CondVal) of
        true -> 
            NewMap = perform_action(Map, Reg, Op, Val);
        false -> 
            NewMap = Map
    end,
    process_ine(Rest, NewMap).
    
main() -> 
   process_line(read_lines("data.txt"), maps:new()).
