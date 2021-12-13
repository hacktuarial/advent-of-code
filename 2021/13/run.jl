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
    dim = maximum(map(maximum, dots)) + 1
    dot_matrix = zeros(Int, (dim, dim))
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
    for i=1:(dim-y)
        out[y - i, :] += mat[y+i, :]
    end
    out
end

actual = foldUp([ 0 0 0 0; 1 0 1 0; 0 1 0 1; 1 1 1 1], 2)
@assert  actual== [0 0 0 0; 2 1 2 1] 


actual = foldUp([0 0 0 1 0 0 1 0 0 1 0 0 0 0 0; 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 1 0 0 0 0 1 0 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 1 0 0 0 0 1 0 1 1 0 0 0 0 0; 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0], 7) 
expected = [1 0 1 1 0 0 1 0 0 1 0 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 1 0 1 0 0 1 0 2 1 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
@assert actual == expected
@assert nonZero(expected) === 17


@assert foldLeft([1 0 1 1 0 0 1 0 0 1 0 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 1 0 1 0 0 1 0 2 1 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; 0 1 0 1 0 0 1 0 2 1 1 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0; 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0],
5) == [1 1 1 1 1; 1 0 0 0 1; 1 0 0 0 1; 1 0 0 0 1; 1 1 1 1 1; 0 0 0 0 0; 0 0 0 0 0]

function part1(fname::String)
    paper = createDotMatrix(readInput(fname))
    paper = foldUp(paper, 7)
    # paper = foldLeft(paper, 5)
    # println(paper)
end

part1("sample.txt")