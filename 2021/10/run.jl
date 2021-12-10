

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
    

@assert score(']') == 57

function find(arr, elt)::Int
    for (i, a) in enumerate(arr)
        if a == elt
            return i
        end
    end
    return -1
end

function isValid(chunk::String)
    empty_char::Char = 'z'
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
    return empty_char
end

@assert isValid("()") == 'z'
@assert isValid("(())") == 'z'
@assert isValid("(((") == 'z'
# @assert isValid(")")
@assert isValid("(((((((((())))))))))") == 'z'

@assert isValid("([])") == 'z'
@assert isValid("([]{}<>)") == 'z'

@assert isValid("{([(<{}[<>[]}>{[]{[(<()>") == '}'
@assert isValid("[[<[([]))<([[{}[[()]]]") == ')'


open("sample_input.txt", "r") do f
    lines = readlines(f)
    corrupted = map(isValid, lines)
    total = reduce((x, y) -> x+y, map(score, corrupted))
    @assert total == 26397
end

open("input.txt", "r") do f
    lines = readlines(f)
    corrupted = map(isValid, lines)
    total = reduce((x, y) -> x+y, map(score, corrupted))
    println(total)
end