using Pipe


function parseNumbers(xy::String, delimiter::Char=',')
    (x, y) = split(xy, delimiter)
    [parse(Int, x), parse(Int, y)]
end

function isDot(line::String)::Bool
    match(r"[0-9]+,[0-9]+", line) !== nothing
end

function nonZero(mat::Array{Int})
    total = 0
    for i=1:size(mat, 1)
        for j=1:size(mat, 2)
            if mat[i, j] > 0
                total += 1
            end
        end
    end
    total
end

function createDotMatrix(dots)
    n_cols = maximum(map(x -> x[1], dots)) + 1
    n_rows = maximum(map(x -> x[2], dots)) + 1
    dot_matrix = zeros(Int, (n_rows, n_cols))
    for (col, row) in dots
        # julia starts indexing at 1 :)
        col += 1
        row += 1
        dot_matrix[row, col] = 1
    end
    dot_matrix
end

function readInput(fname::String)
    open(fname, "r") do f
        lines = readlines(f)
        dots = filter(isDot, lines)
        # folds = filter(line -> ! isDot(line), lines)
        dots = map(parseNumbers, dots)
        return dots
    end
end

function foldUp(mat::Array{Int}, y::Int)::Array{Int}
    y += 1  # julia starts indexing at 1
    dim = size(mat, 1)
    out = copy(mat[1:(y-1), :])
    rows_to_copy = dim - y
    for i = 1:rows_to_copy
        from = y + i
        to = y - i
        out[to, :] += mat[from, :]
    end
    out
end

function foldLeft(mat::Array{Int}, x::Int)::Array{Int}
    x += 1  # julia starts indexing at 1
    dim = size(mat, 2)
    out = copy(mat[:, 1:(x-1)])
    columns_to_copy = dim - x
    for i = 1:columns_to_copy
        from = x + i
        to = x - i
        out[:, to] += mat[:, from]
    end
    out
end

input = [ 0 0 0 0;
          1 0 1 0;
          0 1 0 1;
          1 1 1 1]
actual = foldUp(input, 2)
expected = [0 0 0 0; 2 1 2 1]
@assert actual == expected

actual = foldLeft(input, 2)
expected = [0 0; 1 0; 0 2; 1 2]
@assert actual == expected


actual = foldUp([0 0 0 1 0 0 1 0 0 1 0 0 0 0 0; 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 1 0 0 0 0 1 0 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 1 0 0 0 0 1 0 1 1 0 0 0 0 0; 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0], 7) 
expected = [1 0 1 1 0 0 1 0 0 1 0 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 1 0 1 0 0 1 0 2 1 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
@assert actual == expected
@assert nonZero(expected) === 17


function part1(fname::String)
    paper = createDotMatrix(readInput(fname))
    @assert size(paper) === (15, 11)
    paper = foldUp(paper, 7)
    @assert size(paper) === (7, 11)
    paper = foldLeft(paper, 5)
    @assert size(paper) === (7, 5)
    return nonZero(paper)
end

function prettyPrint(arr)
    open("result.txt", "w") do f
        for i=1:size(arr, 1)
            for j=1:size(arr, 2)
                if arr[i, j] >= 0
                    write(f, '#')
                else
                    write(f, '.')
                end
            end
            write(f, '\n')
        end
    end
end

part1("sample.txt")
open("input.txt", "r") do f
    paper = createDotMatrix(readInput("input.txt"))
    lines = filter(line -> match(r"[xy]=[0-9]+", line) !== nothing, readlines(f))
    for line in lines
        position = parse(Int, match(r"[0-9]+", line).match)
        if match(r"x=", line) === nothing
            # y means foldUp
            paper = foldUp(paper, position)
        else
            # x means foldLeft
            paper = foldLeft(paper, position)
        end
    end
    prettyPrint(paper)
end
