

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

function isValid(chunk::String)::Bool
    open = '('
    close = ')'
    stack::Array{Char} = []
    for c::Char in chunk
        if c == open
            stack = push!(stack, c)
        else
            try
                d = pop!(stack)
                # close must have matching open
                if d != open
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