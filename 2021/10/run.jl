

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

function isValid(chunk::String)::Bool
    open_chars =  ['(', '{', '[', '<']
    close_chars = [')', '}', ']', '>']
    stack:: Array{Char} = []
    for c::Char in chunk
        if c in open_chars
            stack = push!(stack, c)
        else
            # it's a closing character. figure out which one
            try
                d = pop!(stack)
                # close must have matching open
                if find(open_chars, d) != find(close_chars, c)
                    return false
                end
            catch LoadError
                return false
            end
        end
    end
    # if you get to the end, and there's nothing left, it's valid
    return length(stack) == 0
end

@assert isValid("()")
@assert isValid("(())")
@assert ! isValid("(((")
@assert ! isValid(")")
@assert isValid("(((((((((())))))))))")

@assert isValid("([])")
@assert isValid("([]{}<>)")

@assert ! isValid("{([(<{}[<>[]}>{[]{[(<()>")
@assert ! isValid("[[<[([]))<([[{}[[()]]]")