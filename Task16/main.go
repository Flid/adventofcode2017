package main

import (
    "fmt"
    "io/ioutil"
    "strings"
    "strconv"
)

func exchange(arr []rune, pos1 int, pos2 int) {
    tmp := arr[pos1]
    arr[pos1] = arr[pos2]
    arr[pos2] = tmp
}

func invert(arr []rune, start int, end int) {
    for start < end {
        exchange(arr, start, end)
        start++
        end--
    }
}

func swap(arr []rune, n int) {
    invert(arr, 0, len(arr) - 1 - n)
    invert(arr, len(arr) - n, len(arr) - 1)
    invert(arr, 0, len(arr) - 1)
}


func search(arr []rune, r rune) int {
    for i := 0; i < len(arr); i++ {
        if arr[i] == r {
            return i
        }
    }
    return -1
}

func printArr(arr []rune) {
    for i:=0; i<len(arr); i++ {
        s := fmt.Sprintf("%c", arr[i])
        fmt.Print(s)
    }
    fmt.Println("")
}

func main() {
    // Init data structures
    arr := []rune("abcdefghijklmnop")
    
    // Read the input data
    input, err := ioutil.ReadFile("data.txt")
    
    if err != nil {
        panic(err)
    }
    
    input_ops := strings.Split(string(input), ",")
    
    // Execute operations one by one
    for _, op := range input_ops {
        op = strings.TrimSpace(op)
        switch op[0] {
            case 's':
                val, _ := strconv.Atoi(op[1:])
                swap(arr, val)
            case 'x':
                op_parts := strings.Split(op[1:], "/")
                pos1, _ := strconv.Atoi(op_parts[0])
                pos2, _ := strconv.Atoi(op_parts[1])
                exchange(arr, pos1, pos2)
            case 'p':
                op_parts := strings.Split(op[1:], "/")
                pos1 := search(arr, []rune(op_parts[0])[0])
                pos2 := search(arr, []rune(op_parts[1])[0])
                exchange(arr, pos1, pos2)
                
            default:
                fmt.Println("_")
        }
    }
    
    fmt.Println("After 1 iteration:")
    printArr(arr)
    
    /*
    // Once all the operations are applied,
    // create a mapping of initial positions to positions after one round
    mapping := make(map[int] int)
    
    for i:=0; i<len(arr); i++ {
       mapping[i] = search(arr, (rune)('a' + i)) 
    }
    
    
    tmp_mapping := make(map[int] int)
    
    for k,v := range maps {
        tmp_mapping[k] = v
    }
    
    for i:=0; i<9; i++ {
        tmp_mapping
    }*/
}
