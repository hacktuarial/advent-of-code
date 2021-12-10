# import Pkg; Pkg.add("Pipe")
using Pipe
using Statistics
using Printf

function score(char::Char)::Int
    if char == ')'
        return 3
    elseif char == ']'
        return 57
    elseif char == '}'
        return 1197
    elseif char == '>'
        return 25137
    else
        return 0
    end
end
    

function find(arr, elt)::Int
    for (i, a) in enumerate(arr)
        if a == elt
            return i
        end
    end
    return -1
end

function findCorruptCharacter(chunk::String)
    open_chars::Array{Char} =  ['(', '{', '[', '<']
    close_chars ::Array{Char}= [')', '}', ']', '>']
    stack:: Array{Char} = []
    for c::Char in chunk
        if c in open_chars
            stack = push!(stack, c)
        else
            # c is a closing character
            try
                d = pop!(stack)
                # close must have matching open
                if find(open_chars, d) != find(close_chars, c)
                    return c
                end
            catch LoadError
                return false
            end
        end
    end
    # if stack is empty, chunk is valid
    # otherwise, chunk is incomplete
    return stack
end

function isValid(chunk::String)::Bool
    c = findCorruptCharacter(chunk)
    if c isa Char
        return false
    elseif c isa Array{Char}
        return length(c) == 0
    end
end

function isCorrupted(chunk::String)::Bool
    c = findCorruptCharacter(chunk)
    c isa Char
end

function isIncomplete(chunk::String)::Bool
    c = findCorruptCharacter(chunk)
    if c isa Char
        return false
    elseif c isa Array{Char}
        return length(c) > 0
    end
end

@assert isValid("()")
@assert isValid("(())")
@assert isIncomplete("(((")
@assert isValid("(((((((((())))))))))")

@assert isValid("([])")
@assert isValid("([]{}<>)")

@assert findCorruptCharacter("{([(<{}[<>[]}>{[]{[(<()>") == '}'
@assert findCorruptCharacter("[[<[([]))<([[{}[[()]]]") == ')'


function part1(fname::String)::Int
    open(fname, "r") do f
        @pipe readlines(f) |>
        filter(isCorrupted, _) |>
        map(findCorruptCharacter, _) |>
        map(score, _) |>
        reduce((x, y) -> x+y, _)
    end
end


@assert part1("sample_input.txt") == 26397
@assert part1("input.txt") == 392421


function scoreCompletionString(string::String)::Int
    char_scores = Dict(')'=>1, ']'=>2, '}'=>3, '>'=>4)
    score = 0
    for c::Char in string
        score = 5 * score + char_scores[c]
    end
    score
end

@assert scoreCompletionString("}}]])})]") == 288957

function makeCompletionString(stack::Array{Char})
    result::Array{Char} = []
    open_chars::Array{Char} =  ['(', '{', '[', '<']
    close_chars ::Array{Char}= [')', '}', ']', '>']
    while length(stack) > 0
        index = find(open_chars, pop!(stack))
        result = push!(result, close_chars[index])
    end
    join(result)
end

@assert makeCompletionString(['(', '{']) == "})"


function part2(fname::String)
    open(fname, "r") do f
        @pipe readlines(f) |> 
        filter(isIncomplete, _) |>
        map(findCorruptCharacter, _) |>
        map(makeCompletionString, _) |>
        map(scoreCompletionString, _) |>
        median
    end
end
@assert part2("sample_input.txt") == 288957
@assert part2("input.txt") == 2769449099 