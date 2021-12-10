
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
    # if you get to the end, and there's nothing left, it's valid
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


# part1
open("sample_input.txt", "r") do f
    lines = filter(isCorrupted, readlines(f))
    corrupted = map(findCorruptCharacter, lines)
    total = reduce((x, y) -> x+y, map(score, corrupted))
    @assert total == 26397
end

open("input.txt", "r") do f
    lines = filter(isCorrupted, readlines(f))
    corrupted = map(findCorruptCharacter, lines)
    total = reduce((x, y) -> x+y, map(score, corrupted))
    @assert total == 392421
end


# part2

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


open("sample_input.txt", "r") do f
    lines = filter(isIncomplete, readlines(f))
    stacks = map(findCorruptCharacter, lines)
    completions  = map(makeCompletionString, stacks)
    scores = map(scoreCompletionString, completions)
    @assert median(scores) == 288957
end

open("input.txt", "r") do f
    lines = filter(isIncomplete, readlines(f))
    stacks = map(findCorruptCharacter, lines)
    completions  = map(makeCompletionString, stacks)
    scores = map(scoreCompletionString, completions)
    @assert median(scores) == 2769449099 
    # @printf "%d" median(scores)
end