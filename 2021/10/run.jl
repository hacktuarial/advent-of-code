

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
    open_chars = ['(', '{', '[', '<']
    close_chars = [')', '}', ']', '>']
    stacks::Array{Array{Char}} = [[], [], [], []]
    for c::Char in chunk
        if c in open_chars
            index = find(open_chars, c)
            stacks[index] = push!(stacks[index], c)
        else
            # it's a closing character. figure out which one
            index = find(close_chars, c)
            try
                d = pop!(stacks[index])
                # close must have matching open
                if d != open_chars[index]
                    return false
                end
            catch LoadError
                return false
            end
        end
    end
    # if you get to the end, and there's nothing left, it's valid
    return all(length(stack) == 0 for stack in stacks)
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